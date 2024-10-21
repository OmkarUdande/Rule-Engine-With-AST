from django.shortcuts import render
from django.http import JsonResponse
from .models import Rule, User
import ast

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type
        self.left = left
        self.right = right
        self.value = value

def parse_rule(expression):
    tree = ast.parse(expression, mode='eval')
    return convert_ast_to_node(tree.body)

def convert_ast_to_node(expr):
    if isinstance(expr, ast.BoolOp):
        op_type = 'AND' if isinstance(expr.op, ast.And) else 'OR'
        left = convert_ast_to_node(expr.values[0])
        right = convert_ast_to_node(expr.values[1])
        return Node('operator', left, right, op_type)
    elif isinstance(expr, ast.Compare):
        left = expr.left.id
        right = expr.comparators[0].n
        return Node('operand', value=f"{left} {ast.dump(expr.ops[0])} {right}")
    else:
        raise NotImplementedError(f"Unsupported expression: {expr}")

def evaluate_rule(ast_node, user_data):
    if ast_node.type == 'operand':
        condition = ast_node.value
        return eval(condition, {}, user_data)
    elif ast_node.type == 'operator':
        left_result = evaluate_rule(ast_node.left, user_data)
        right_result = evaluate_rule(ast_node.right, user_data)
        if ast_node.value == 'AND':
            return left_result and right_result
        elif ast_node.value == 'OR':
            return left_result or right_result

def validate_rule(rule_text):
    required_attributes = ['age', 'department', 'salary', 'experience']
    if not all(attr in rule_text for attr in required_attributes):
        missing_attrs = [attr for attr in required_attributes if attr not in rule_text]
        return False, f"Missing required attributes: {', '.join(missing_attrs)}"
    return True, ""



def create_rule(request):
    if request.method == 'POST':
        rule_text = request.POST.get('rule_text')
        print(f"Submitted rule_text: {rule_text}")  # Debug print
        if not rule_text:
            return render(request, 'create_rule.html', {'error': 'No rule text provided'})

        # Validate the rule before parsing
        is_valid, error_message = validate_rule(rule_text)
        print(f"Validation result: {is_valid}, Error message: {error_message}")  # Debug print
        if not is_valid:
            return render(request, 'create_rule.html', {'error': error_message})

        # Mock user data for testing
        mock_user_data = {
            'age': 25,
            'department': 'HR',
            'salary': 50000,
            'experience': 2
        }

        try:
        
            rule_text = rule_text.replace("AND", "and").replace("OR", "or")
            
            # Test eval to check if the syntax is valid
            eval_result = eval(f"({rule_text})", {}, mock_user_data)  # Provide the mock user data
            print(f"Eval result: {eval_result}")  # Debug print

            # Parse and convert the rule to an AST representation
            tree = ast.parse(rule_text, mode='eval')
            ast_json = ast.dump(tree)

            # If no errors, save the rule with the AST
            rule = Rule(rule_text=rule_text, ast=ast_json)  # Save both rule text and AST
            rule.save()

            return JsonResponse({'message': 'Rule created successfully', 'rule': rule_text})

        except SyntaxError as e:
            return render(request, 'create_rule.html', {'error': f'Invalid rule syntax: {e}'})
        except Exception as e:
            return render(request, 'create_rule.html', {'error': f'Error evaluating rule: {e}'})

    return render(request, 'create_rule.html')



def evaluate(request, user_id):
    user = User.objects.get(id=user_id)
    rule = Rule.objects.first()  # first rule 
    ast_rule = parse_rule(rule.rule_text)

    user_data = {
        'age': user.age,
        'department': user.department,
        'salary': user.salary,
        'experience': user.experience
    }

    result = evaluate_rule(ast_rule, user_data)
    return JsonResponse({'eligible': result})
