from gavel.dialects.base.parser import LogicParser
from gavel.dialects.base.parser import Parseable
from gavel.dialects.base.parser import ProblemParser
from gavel.dialects.tptp.parser import TPTPParser
from gavel.logic import logic, problem


class DBProblemParser(ProblemParser):
    logic_parser_cls = LogicParser

    def __init__(self, *args, **kwargs):
        super(DBProblemParser, self).__init__(*args, **kwargs)
        self.logic_parser = LogicParser()

    def parse(self, structure: Parseable, *args, **kwargs):
        premises = [self.logic_parser.parse(s) for s in structure.premises]
        conjecture = self.logic_parser.parse(structure.conjecture)
        return logic.Problem(premises, conjecture)


class DBLogicParser(LogicParser):
    def _parse_rec(self, obj, *args, **kwargs):
        if isinstance(obj, str):
            if obj == "$true":
                return logic.DefinedConstant(logic.PredefinedConstant.VERUM)
            if obj == "$false":
                return logic.DefinedConstant(logic.PredefinedConstant.FALSUM)
            return obj
        meth = getattr(self, "parse_%s" % obj.get("type"), None)

        if meth is None:
            raise Exception(
                "Parser '{name}' not found for {cls}".format(
                    name=obj.get("type"), cls=obj
                )
            )
        return meth(obj)

    def parse_quantifier(self, quantifier: dict):
        if quantifier.get("quantifier") == "existential":
            return logic.Quantifier.EXISTENTIAL
        elif quantifier.get("quantifier") == "universial":
            return logic.Quantifier.UNIVERSAL
        else:
            raise NotImplementedError

    def parse_formula_role(self, role: dict):
        return getattr(logic.FormulaRole, role["formula_role"].upper())

    def parse_binary_connective(self, connective: dict):
        return getattr(logic.BinaryConnective, connective["binary_connective"].upper())

    def parse_defined_predicate(self, predicate: dict):
        return getattr(logic.DefinedPredicate, predicate["defined_predicate"].upper())

    def parse_unary_connective(self, connective: dict):
        return getattr(logic.UnaryConnective, connective["unary_connective"].upper())

    def parse_unary_formula(self, formula: dict):
        return logic.UnaryFormula(
            formula=self._parse_rec(formula["formula"]),
            connective=self._parse_rec(formula["connective"]),
        )

    def parse_quantified_formula(self, formula: dict):
        return logic.QuantifiedFormula(
            formula=self._parse_rec(formula["formula"]),
            quantifier=self._parse_rec(formula["quantifier"]),
            variables=[self._parse_rec(v) for v in formula["quantifier"]],
        )

    def parse_annotated_formula(self, anno: dict):
        return problem.AnnotatedFormula(
            formula=self._parse_rec(anno["formula"]),
            name=anno["name"],
            role=self._parse_rec(anno["role"]),
            logic=anno["logic"],
        )

    def parse_binary_formula(self, formula: dict):
        return logic.BinaryFormula(
            left=self._parse_rec(formula["left"]),
            right=self._parse_rec(formula["right"]),
            operator=self._parse_rec(formula["connective"]),
        )

    def parse_functor_expression(self, expression: logic.FunctorExpression):
        return logic.FunctorExpression(
            functor=self._parse_rec(expression["functor"]),
            arguments=[self._parse_rec(a) for a in expression["arguments"]],
        )

    def parse_predicate_expression(self, expression: dict) -> logic.PredicateExpression:
        return logic.PredicateExpression(
            predicate=self._parse_rec(expression["predicate"]),
            arguments=[self._parse_rec(a) for a in expression["arguments"]],
        )

    def parse_conditional(self, conditional: dict) -> logic.Conditional:
        return logic.Conditional(
            if_clause=self._parse_rec(conditional["if_clause"]),
            then_clause=self._parse_rec(conditional["then_clause"]),
            else_clause=self._parse_rec(conditional["else_clause"]),
        )

    def parse_import(self, imp: dict) -> problem.Import:
        return logic.Import(path=imp["path"])

    def parse_variable(self, variable: dict) -> logic.Variable:
        return logic.Variable(symbol=variable["symbol"])

    def parse_constant(self, variable: dict):
        return logic.Constant(symbol=variable["symbol"])

    def parse_problem(self, problem: dict) -> problem.Problem:
        return problem.Problem(
            premises=[self._parse_rec(p) for p in problem["premises"]],
            conjecture=self._parse_rec(problem["conjecture"]),
            imports=self._parse_rec(problem["imports"]),
        )

    def parse_distinct_object(self, obj):
        return logic.DistinctObject(obj["symbol"])
