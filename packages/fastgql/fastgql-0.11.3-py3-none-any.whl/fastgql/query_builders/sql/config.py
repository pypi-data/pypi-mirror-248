import typing as T
import inspect
from dataclasses import dataclass
from pydantic import TypeAdapter

from fastgql.info import Info
from fastgql.gql_ast import models as M
from fastgql.execute.utils import parse_value
from fastgql.utils import node_from_path
from .query_builder import QueryBuilder, Cardinality


def combine_qbs(
    *qbs: QueryBuilder,
    nodes_to_include: list[
        M.FieldNode
    ],  # TODO so far, not needed but may for better inheritence
) -> QueryBuilder:
    """takes in a dict of db typename and qb"""
    new_qb = QueryBuilder()
    # add dangling to each qb
    for node in nodes_to_include:
        for qb in qbs:
            if node.name == "__typename":
                qb.fields.add(f"{node.alias or node.name} := .__type__.name")
            # TODO other things here
    for qb in qbs:
        if not qb.typename:
            raise Exception("QB must have a typename if it is to be combined.")
        new_qb.children[qb.typename] = ChildEdge(
            db_expression=f"[is {qb.typename}]", qb=qb
        )
    return new_qb


@dataclass
class Property:
    path: str | None
    update_qb: T.Callable[[QueryBuilder], T.Awaitable[None] | None] = None


@dataclass
class Link:
    # table_name: str | None
    from_: str | None
    cardinality: Cardinality

    return_cls_qb_config: (
        T.Union["QueryBuilderConfig", dict[str, "QueryBuilderConfig"]] | None
    ) = None
    path_to_return_cls: tuple[str, ...] | None = None
    update_qbs: T.Callable[[..., T.Any], None | T.Awaitable] = None


@dataclass
class QueryBuilderConfig:
    table_name: str

    properties: dict[str, Property]
    links: dict[str, Link]

    def is_empty(self) -> bool:
        return not self.properties and not self.links

    async def from_info(
        self,
        info: Info,
        node: M.FieldNode | M.InlineFragmentNode,
        cardinality: Cardinality,
    ) -> QueryBuilder | None:
        # TODO
        if not node:
            return None
        qb = QueryBuilder(table_name=self.table_name, cardinality=cardinality)
        children_q = [*node.children]
        while len(children_q) > 0:
            child = children_q.pop(0)
            if isinstance(child, M.InlineFragmentNode):
                children_q.extend(child.children)
            else:
                if child.name in self.properties:
                    property_config = self.properties[child.name]

                    if path_to_value := property_config.path:
                        qb.sel(name=child.name, path=path_to_value)
                    if update_qb := property_config.update_qb:
                        kwargs = {
                            "qb": qb,
                            "node": node,
                            "child_node": child,
                            "info": info,
                            **{
                                a.name: parse_value(
                                    variables=info.context.variables, v=a.value
                                )
                                for a in child.arguments
                            },
                        }
                        kwargs = {
                            k: v
                            for k, v in kwargs.items()
                            if k in inspect.signature(update_qb).parameters
                        }
                        _ = update_qb(**kwargs)
                        if inspect.isawaitable(_):
                            await _
                if child.name in self.links:
                    method_config = self.links[child.name]
                    original_child = child
                    if method_config.path_to_return_cls:
                        child = node_from_path(
                            node=child, path=[*method_config.path_to_return_cls]
                        )
                    if config := method_config.return_cls_qb_config:
                        # TODO DO NOT WORRY ABOUT THIS FOR NOW
                        if isinstance(config, dict):
                            dangling_children: list[M.FieldNode] = []
                            frag_qbs: list[QueryBuilder] = []
                            for child_child in child.children:
                                if isinstance(child_child, M.InlineFragmentNode):
                                    child_child_qb = await config[
                                        child_child.type_condition
                                    ].from_info(
                                        info=info,
                                        node=child_child,
                                        cardinality=Cardinality.ONE,
                                    )  # TODO LATER
                                    child_child_qb.typename = child_child.type_condition
                                    frag_qbs.append(child_child_qb)
                                elif isinstance(child_child, M.FieldNode):
                                    dangling_children.append(child_child)
                                else:
                                    raise Exception(
                                        f"Invalid node for config as dict: {child=}"
                                    )
                            # now combine the dangling with the frags
                            child_qb = combine_qbs(
                                *frag_qbs, nodes_to_include=dangling_children
                            )
                            # child_qb.fields.add("typename := .__type__.name") # TODO
                        else:
                            child_qb = await config.from_info(
                                info=info,
                                node=child,
                                cardinality=method_config.cardinality,
                            )  # TODO LATER

                        if from_where := method_config.from_:
                            child_qb.from_ = from_where
                            qb.sel_sub(
                                name=child.alias or child.name,
                                qb=child_qb,
                            )

                        if update_qbs := method_config.update_qbs:
                            new_kwargs: dict[str, T.Any] = {}
                            sig = inspect.signature(update_qbs)
                            args_by_name: dict[str, M.Argument] = {
                                a.name: a for a in original_child.arguments
                            }
                            for name, param in sig.parameters.items():
                                if name in args_by_name:
                                    arg = args_by_name[name]
                                    val = arg.value
                                    if val is not None:
                                        # TODO get use camel case...
                                        val = TypeAdapter(
                                            param.annotation
                                        ).validate_python(
                                            val, context={"_use_camel_case": True}
                                        )
                                    new_kwargs[name] = val
                                elif name == "qb":
                                    new_kwargs[name] = qb
                                elif name == "child_qb":
                                    new_kwargs[name] = child_qb
                                elif name == "node":
                                    new_kwargs[name] = node
                                elif name == "child_node":
                                    new_kwargs[name] = child
                                elif name == "info":
                                    new_kwargs[name] = info
                                elif name == "original_child":
                                    new_kwargs[name] = original_child

                            _ = update_qbs(**new_kwargs)
                            if inspect.isawaitable(_):
                                await _
        return qb
