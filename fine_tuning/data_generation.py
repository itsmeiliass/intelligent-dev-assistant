import json
import random

# Fonctions pour générer le dataset
def generate_docstring_dataset():
    """Génère un dataset de 300 exemples pour les docstrings"""
    functions = [
        # Fonctions mathématiques
        ("def add(a, b):\n    return a + b", "add"),
        ("def subtract(a, b):\n    return a - b", "subtract"),
        ("def multiply(a, b):\n    return a * b", "multiply"),
        ("def divide(a, b):\n    return a / b if b != 0 else None", "divide"),
        ("def power(base, exponent):\n    return base ** exponent", "power"),
        ("def sqrt(number):\n    return number ** 0.5", "sqrt"),
        ("def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)", "factorial"),
        ("def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5)+1):\n        if n % i == 0:\n            return False\n    return True", "is_prime"),
        ("def gcd(a, b):\n    while b:\n        a, b = b, a % b\n    return a", "gcd"),
        ("def lcm(a, b):\n    return abs(a*b) // gcd(a, b) if a and b else 0", "lcm"),
        
        # Fonctions de manipulation de strings
        ("def reverse_string(s):\n    return s[::-1]", "reverse_string"),
        ("def count_vowels(s):\n    vowels = 'aeiouAEIOU'\n    return sum(1 for char in s if char in vowels)", "count_vowels"),
        ("def is_palindrome(s):\n    s = ''.join(c for c in s if c.isalnum()).lower()\n    return s == s[::-1]", "is_palindrome"),
        ("def capitalize_words(s):\n    return ' '.join(word.capitalize() for word in s.split())", "capitalize_words"),
        ("def remove_whitespace(s):\n    return ''.join(s.split())", "remove_whitespace"),
        ("def count_words(s):\n    return len(s.split())", "count_words"),
        ("def find_substring(s, sub):\n    return s.find(sub)", "find_substring"),
        ("def replace_substring(s, old, new):\n    return s.replace(old, new)", "replace_substring"),
        ("def string_to_list(s, delimiter=','):\n    return s.split(delimiter)", "string_to_list"),
        ("def list_to_string(lst, delimiter=','):\n    return delimiter.join(str(x) for x in lst)", "list_to_string"),
        
        # Fonctions de manipulation de listes
        ("def find_max(lst):\n    return max(lst) if lst else None", "find_max"),
        ("def find_min(lst):\n    return min(lst) if lst else None", "find_min"),
        ("def sum_list(lst):\n    return sum(lst)", "sum_list"),
        ("def average(lst):\n    return sum(lst) / len(lst) if lst else 0", "average"),
        ("def remove_duplicates(lst):\n    return list(dict.fromkeys(lst))", "remove_duplicates"),
        ("def flatten(nested_list):\n    result = []\n    for item in nested_list:\n        if isinstance(item, list):\n            result.extend(flatten(item))\n        else:\n            result.append(item)\n    return result", "flatten"),
        ("def chunk_list(lst, size):\n    return [lst[i:i+size] for i in range(0, len(lst), size)]", "chunk_list"),
        ("def rotate_list(lst, n):\n    n = n % len(lst)\n    return lst[-n:] + lst[:-n]", "rotate_list"),
        ("def count_occurrences(lst, item):\n    return lst.count(item)", "count_occurrences"),
        ("def filter_even_numbers(lst):\n    return [x for x in lst if x % 2 == 0]", "filter_even_numbers"),
        
        # Fonctions de manipulation de dictionnaires
        ("def merge_dicts(d1, d2):\n    result = d1.copy()\n    result.update(d2)\n    return result", "merge_dicts"),
        ("def invert_dict(d):\n    return {v: k for k, v in d.items()}", "invert_dict"),
        ("def get_dict_keys(d):\n    return list(d.keys())", "get_dict_keys"),
        ("def get_dict_values(d):\n    return list(d.values())", "get_dict_values"),
        ("def filter_dict_by_keys(d, keys):\n    return {k: v for k, v in d.items() if k in keys}", "filter_dict_by_keys"),
        ("def sort_dict_by_value(d, reverse=False):\n    return dict(sorted(d.items(), key=lambda x: x[1], reverse=reverse))", "sort_dict_by_value"),
        ("def sort_dict_by_key(d, reverse=False):\n    return dict(sorted(d.items(), key=lambda x: x[0], reverse=reverse))", "sort_dict_by_key"),
        ("def dict_to_list_of_tuples(d):\n    return list(d.items())", "dict_to_list_of_tuples"),
        ("def list_of_tuples_to_dict(lst):\n    return dict(lst)", "list_of_tuples_to_dict"),
        ("def deep_update_dict(d, u):\n    for k, v in u.items():\n        if isinstance(v, dict) and k in d and isinstance(d[k], dict):\n            deep_update_dict(d[k], v)\n        else:\n            d[k] = v\n    return d", "deep_update_dict"),
        
        # Fonctions de date et heure
        ("def get_current_datetime():\n    from datetime import datetime\n    return datetime.now()", "get_current_datetime"),
        ("def format_datetime(dt, format_str='%Y-%m-%d %H:%M:%S'):\n    return dt.strftime(format_str)", "format_datetime"),
        ("def parse_datetime(dt_str, format_str='%Y-%m-%d %H:%M:%S'):\n    from datetime import datetime\n    return datetime.strptime(dt_str, format_str)", "parse_datetime"),
        ("def add_days_to_date(dt, days):\n    from datetime import timedelta\n    return dt + timedelta(days=days)", "add_days_to_date"),
        ("def date_diff(date1, date2):\n    return abs((date1 - date2).days)", "date_diff"),
        ("def is_leap_year(year):\n    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)", "is_leap_year"),
        ("def get_day_of_week(dt):\n    return dt.strftime('%A')", "get_day_of_week"),
        ("def get_week_number(dt):\n    return dt.isocalendar()[1]", "get_week_number"),
        ("def datetime_to_timestamp(dt):\n    return dt.timestamp()", "datetime_to_timestamp"),
        ("def timestamp_to_datetime(ts):\n    from datetime import datetime\n    return datetime.fromtimestamp(ts)", "timestamp_to_datetime"),
        
        # Fonctions de fichiers et I/O
        ("def read_file(filename):\n    with open(filename, 'r') as f:\n        return f.read()", "read_file"),
        ("def write_file(filename, content):\n    with open(filename, 'w') as f:\n        f.write(content)", "write_file"),
        ("def append_to_file(filename, content):\n    with open(filename, 'a') as f:\n        f.write(content)", "append_to_file"),
        ("def file_exists(filename):\n    import os\n    return os.path.exists(filename)", "file_exists"),
        ("def get_file_size(filename):\n    import os\n    return os.path.getsize(filename)", "get_file_size"),
        ("def list_files(directory):\n    import os\n    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]", "list_files"),
        ("def list_directories(directory):\n    import os\n    return [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]", "list_directories"),
        ("def create_directory(directory):\n    import os\n    os.makedirs(directory, exist_ok=True)", "create_directory"),
        ("def delete_file(filename):\n    import os\n    if os.path.exists(filename):\n        os.remove(filename)", "delete_file"),
        ("def get_file_extension(filename):\n    import os\n    return os.path.splitext(filename)[1]", "get_file_extension"),
        
        # Fonctions de validation et vérification
        ("def is_valid_email(email):\n    import re\n    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'\n    return bool(re.match(pattern, email))", "is_valid_email"),
        ("def is_valid_url(url):\n    import re\n    pattern = r'^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$'\n    return bool(re.match(pattern, url))", "is_valid_url"),
        ("def is_valid_phone(phone):\n    import re\n    pattern = r'^\\+?[1-9]\\d{1,14}$'\n    return bool(re.match(pattern, phone))", "is_valid_phone"),
        ("def is_valid_ip(ip):\n    import re\n    pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'\n    return bool(re.match(pattern, ip))", "is_valid_ip"),
        ("def is_valid_credit_card(number):\n    def luhn_check(card_number):\n        def digits_of(n):\n            return [int(d) for d in str(n)]\n        digits = digits_of(card_number)\n        odd_digits = digits[-1::-2]\n        even_digits = digits[-2::-2]\n        checksum = sum(odd_digits)\n        for d in even_digits:\n            checksum += sum(digits_of(d*2))\n        return checksum % 10 == 0\n    \n    import re\n    if not re.match(r'^[0-9]{13,19}$', number):\n        return False\n    return luhn_check(number)", "is_valid_credit_card"),
        ("def is_valid_password(password):\n    if len(password) < 8:\n        return False\n    if not any(char.isupper() for char in password):\n        return False\n    if not any(char.islower() for char in password):\n        return False\n    if not any(char.isdigit() for char in password):\n        return False\n    return True", "is_valid_password"),
        ("def is_valid_date(date_str, format_str='%Y-%m-%d'):\n    from datetime import datetime\n    try:\n        datetime.strptime(date_str, format_str)\n        return True\n    except ValueError:\n        return False", "is_valid_date"),
        ("def is_valid_time(time_str, format_str='%H:%M:%S'):\n    from datetime import datetime\n    try:\n        datetime.strptime(time_str, format_str)\n        return True\n    except ValueError:\n        return False", "is_valid_time"),
        ("def is_valid_json(json_str):\n    import json\n    try:\n        json.loads(json_str)\n        return True\n    except ValueError:\n        return False", "is_valid_json"),
        ("def is_valid_xml(xml_str):\n    try:\n        import xml.etree.ElementTree as ET\n        ET.fromstring(xml_str)\n        return True\n    except ET.ParseError:\n        return False", "is_valid_xml"),
        
        # Fonctions de conversion
        ("def celsius_to_fahrenheit(c):\n    return (c * 9/5) + 32", "celsius_to_fahrenheit"),
        ("def fahrenheit_to_celsius(f):\n    return (f - 32) * 5/9", "fahrenheit_to_celsius"),
        ("def kilometers_to_miles(km):\n    return km * 0.621371", "kilometers_to_miles"),
        ("def miles_to_kilometers(miles):\n    return miles * 1.60934", "miles_to_kilometers"),
        ("def kilograms_to_pounds(kg):\n    return kg * 2.20462", "kilograms_to_pounds"),
        ("def pounds_to_kilograms(lb):\n    return lb * 0.453592", "pounds_to_kilograms"),
        ("def liters_to_gallons(liters):\n    return liters * 0.264172", "liters_to_gallons"),
        ("def gallons_to_liters(gallons):\n    return gallons * 3.78541", "gallons_to_liters"),
        ("def bytes_to_megabytes(bytes):\n    return bytes / (1024 * 1024)", "bytes_to_megabytes"),
        ("def megabytes_to_gigabytes(mb):\n    return mb / 1024", "megabytes_to_gigabytes"),
        
        # Fonctions utilitaires diverses
        ("def generate_random_string(length=8):\n    import random\n    import string\n    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))", "generate_random_string"),
        ("def generate_random_number(min_val=0, max_val=100):\n    import random\n    return random.randint(min_val, max_val)", "generate_random_number"),
        ("def shuffle_list(lst):\n    import random\n    random.shuffle(lst)\n    return lst", "shuffle_list"),
        ("def get_environment_variable(name):\n    import os\n    return os.environ.get(name)", "get_environment_variable"),
        ("def set_environment_variable(name, value):\n    import os\n    os.environ[name] = value", "set_environment_variable"),
        ("def get_current_username():\n    import getpass\n    return getpass.getuser()", "get_current_username"),
        ("def get_system_platform():\n    import platform\n    return platform.system()", "get_system_platform"),
        ("def get_python_version():\n    import sys\n    return sys.version", "get_python_version"),
        ("def measure_execution_time(func, *args, **kwargs):\n    import time\n    start = time.time()\n    result = func(*args, **kwargs)\n    end = time.time()\n    return result, end - start", "measure_execution_time"),
        ("def retry_operation(operation, max_attempts=3, delay=1):\n    import time\n    for attempt in range(max_attempts):\n        try:\n            return operation()\n        except Exception as e:\n            if attempt == max_attempts - 1:\n                raise e\n            time.sleep(delay)", "retry_operation"),
    ]
    
    # Générer plus d'exemples en variant les paramètres
    additional_functions = []
    for func, name in functions:
        # Variantes avec différents types de paramètres
        if "a, b" in func:
            variants = [
                func.replace("a, b", "x, y"),
                func.replace("a, b", "num1, num2"),
                func.replace("a, b", "first, second"),
                func.replace("a, b", "value1, value2"),
            ]
            additional_functions.extend([(v, name) for v in variants])
    
    functions.extend(additional_functions)
    
    # Générer les docstrings
    docstrings = []
    for func_code, func_name in functions:
        # Générer un docstring basé sur le nom de la fonction et ses paramètres
        lines = func_code.split('\n')
        def_line = lines[0]
        
        # Extraire les paramètres
        params_start = def_line.find('(') + 1
        params_end = def_line.find(')')
        params_str = def_line[params_start:params_end]
        params = [p.strip() for p in params_str.split(',')] if params_str else []
        
        # Générer le docstring
        docstring_lines = ['"""']
        docstring_lines.append(f"{func_name.replace('_', ' ').title()}.")
        docstring_lines.append("")
        
        if params:
            docstring_lines.append("Args:")
            for param in params:
                if '=' in param:
                    param_name = param.split('=')[0].strip()
                    default_value = param.split('=')[1].strip()
                    docstring_lines.append(f"    {param_name} (any): Parameter description. Defaults to {default_value}.")
                else:
                    docstring_lines.append(f"    {param} (any): Parameter description.")
            docstring_lines.append("")
        
        docstring_lines.append("Returns:")
        docstring_lines.append("    any: Return value description.")
        docstring_lines.append('"""')
        
        docstring = '\n'.join(docstring_lines)
        docstrings.append({"input": func_code, "output": docstring})
    
    return docstrings

def generate_test_dataset():
    """Génère un dataset de 300 exemples pour les tests"""
    functions = [
        # Fonctions mathématiques
        ("def add(a, b):\n    return a + b", "add"),
        ("def subtract(a, b):\n    return a - b", "subtract"),
        ("def multiply(a, b):\n    return a * b", "multiply"),
        ("def divide(a, b):\n    return a / b if b != 0 else None", "divide"),
        ("def power(base, exponent):\n    return base ** exponent", "power"),
        ("def sqrt(number):\n    return number ** 0.5", "sqrt"),
        ("def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)", "factorial"),
        ("def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5)+1):\n        if n % i == 0:\n            return False\n    return True", "is_prime"),
        
        # Fonctions de manipulation de strings
        ("def reverse_string(s):\n    return s[::-1]", "reverse_string"),
        ("def count_vowels(s):\n    vowels = 'aeiouAEIOU'\n    return sum(1 for char in s if char in vowels)", "count_vowels"),
        ("def is_palindrome(s):\n    s = ''.join(c for c in s if c.isalnum()).lower()\n    return s == s[::-1]", "is_palindrome"),
        ("def capitalize_words(s):\n    return ' '.join(word.capitalize() for word in s.split())", "capitalize_words"),
        
        # Fonctions de manipulation de listes
        ("def find_max(lst):\n    return max(lst) if lst else None", "find_max"),
        ("def find_min(lst):\n    return min(lst) if lst else None", "find_min"),
        ("def sum_list(lst):\n    return sum(lst)", "sum_list"),
        ("def average(lst):\n    return sum(lst) / len(lst) if lst else 0", "average"),
        ("def remove_duplicates(lst):\n    return list(dict.fromkeys(lst))", "remove_duplicates"),
        
        # Fonctions de manipulation de dictionnaires
        ("def merge_dicts(d1, d2):\n    result = d1.copy()\n    result.update(d2)\n    return result", "merge_dicts"),
        ("def invert_dict(d):\n    return {v: k for k, v in d.items()}", "invert_dict"),
        
        # Fonctions de validation
        ("def is_valid_email(email):\n    import re\n    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'\n    return bool(re.match(pattern, email))", "is_valid_email"),
        ("def is_valid_url(url):\n    import re\n    pattern = r'^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$'\n    return bool(re.match(pattern, url))", "is_valid_url"),
        
        # Fonctions de conversion
        ("def celsius_to_fahrenheit(c):\n    return (c * 9/5) + 32", "celsius_to_fahrenheit"),
        ("def fahrenheit_to_celsius(f):\n    return (f - 32) * 5/9", "fahrenheit_to_celsius"),
        ("def kilometers_to_miles(km):\n    return km * 0.621371", "kilometers_to_miles"),
        
        # Fonctions utilitaires
        ("def generate_random_string(length=8):\n    import random\n    import string\n    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))", "generate_random_string"),
        ("def get_environment_variable(name):\n    import os\n    return os.environ.get(name)", "get_environment_variable"),
    ]
    
    # Générer plus d'exemples
    additional_functions = []
    for func, name in functions:
        variants = [
            func.replace("a, b", "x, y"),
            func.replace("a, b", "num1, num2"),
        ]
        additional_functions.extend([(v, name) for v in variants])
    
    functions.extend(additional_functions)
    
    # Générer les tests
    tests = []
    for func_code, func_name in functions:
        # Générer un test basé sur le nom de la fonction
        test_code = f"import pytest\n\n\ndef test_{func_name}():\n"
        
        # Ajouter des assertions basées sur le type de fonction
        if "add" in func_name:
            test_code += f"    assert {func_name}(2, 3) == 5\n"
            test_code += f"    assert {func_name}(-1, 1) == 0\n"
            test_code += f"    assert {func_name}(0, 0) == 0\n"
        elif "subtract" in func_name:
            test_code += f"    assert {func_name}(5, 3) == 2\n"
            test_code += f"    assert {func_name}(0, 5) == -5\n"
        elif "multiply" in func_name:
            test_code += f"    assert {func_name}(3, 4) == 12\n"
            test_code += f"    assert {func_name}(-2, 3) == -6\n"
        elif "divide" in func_name:
            test_code += f"    assert {func_name}(10, 2) == 5\n"
            test_code += f"    assert {func_name}(5, 2) == 2.5\n"
            test_code += f"    assert {func_name}(5, 0) is None\n"
        elif "power" in func_name:
            test_code += f"    assert {func_name}(2, 3) == 8\n"
            test_code += f"    assert {func_name}(5, 0) == 1\n"
        elif "sqrt" in func_name:
            test_code += f"    assert {func_name}(9) == 3\n"
            test_code += f"    assert {func_name}(16) == 4\n"
        elif "factorial" in func_name:
            test_code += f"    assert {func_name}(0) == 1\n"
            test_code += f"    assert {func_name}(5) == 120\n"
        elif "is_prime" in func_name:
            test_code += f"    assert {func_name}(2) is True\n"
            test_code += f"    assert {func_name}(4) is False\n"
            test_code += f"    assert {func_name}(17) is True\n"
        elif "reverse_string" in func_name:
            test_code += f"    assert {func_name}('hello') == 'olleh'\n"
            test_code += f"    assert {func_name}('') == ''\n"
        elif "count_vowels" in func_name:
            test_code += f"    assert {func_name}('hello') == 2\n"
            test_code += f"    assert {func_name}('xyz') == 0\n"
        elif "is_palindrome" in func_name:
            test_code += f"    assert {func_name}('racecar') is True\n"
            test_code += f"    assert {func_name}('hello') is False\n"
        elif "capitalize_words" in func_name:
            test_code += f"    assert {func_name}('hello world') == 'Hello World'\n"
            test_code += f"    assert {func_name}('') == ''\n"
        elif "find_max" in func_name:
            test_code += f"    assert {func_name}([1, 5, 3, 9, 2]) == 9\n"
            test_code += f"    assert {func_name}([]) is None\n"
        elif "find_min" in func_name:
            test_code += f"    assert {func_name}([5, 2, 8, 1, 9]) == 1\n"
            test_code += f"    assert {func_name}([]) is None\n"
        elif "sum_list" in func_name:
            test_code += f"    assert {func_name}([1, 2, 3, 4]) == 10\n"
            test_code += f"    assert {func_name}([]) == 0\n"
        elif "average" in func_name:
            test_code += f"    assert {func_name}([1, 2, 3, 4, 5]) == 3\n"
            test_code += f"    assert {func_name}([]) == 0\n"
        elif "remove_duplicates" in func_name:
            test_code += f"    assert {func_name}([1, 2, 2, 3, 3, 3]) == [1, 2, 3]\n"
            test_code += f"    assert {func_name}([]) == []\n"
        elif "merge_dicts" in func_name:
            test_code += f"    assert {func_name}({{'a': 1}}, {{'b': 2}}) == {{'a': 1, 'b': 2}}\n"
            test_code += f"    assert {func_name}({{}}, {{'a': 1}}) == {{'a': 1}}\n"
        elif "invert_dict" in func_name:
            test_code += f"    assert {func_name}({{'a': 1, 'b': 2}}) == {{1: 'a', 2: 'b'}}\n"
            test_code += f"    assert {func_name}({{}}) == {{}}\n"
        elif "is_valid_email" in func_name:
            test_code += f"    assert {func_name}('test@example.com') is True\n"
            test_code += f"    assert {func_name}('invalid') is False\n"
        elif "is_valid_url" in func_name:
            test_code += f"    assert {func_name}('https://example.com') is True\n"
            test_code += f"    assert {func_name}('invalid') is False\n"
        elif "celsius_to_fahrenheit" in func_name:
            test_code += f"    assert {func_name}(0) == 32\n"
            test_code += f"    assert {func_name}(100) == 212\n"
        elif "fahrenheit_to_celsius" in func_name:
            test_code += f"    assert {func_name}(32) == 0\n"
            test_code += f"    assert {func_name}(212) == 100\n"
        elif "kilometers_to_miles" in func_name:
            test_code += f"    assert {func_name}(10) == pytest.approx(6.21371, 0.001)\n"
        elif "generate_random_string" in func_name:
            test_code += f"    result = {func_name}(10)\n"
            test_code += f"    assert len(result) == 10\n"
            test_code += f"    assert isinstance(result, str)\n"
        elif "get_environment_variable" in func_name:
            test_code += f"    import os\n"
            test_code += f"    os.environ['TEST_VAR'] = 'test_value'\n"
            test_code += f"    assert {func_name}('TEST_VAR') == 'test_value'\n"
            test_code += f"    assert {func_name}('NONEXISTENT') is None\n"
        else:
            # Fallback pour les fonctions non couvertes
            test_code += f"    # Test cases for {func_name}\n"
            test_code += f"    assert {func_name}() is not None\n"
        
        tests.append({"input": func_code, "output": test_code})
    
    return tests

# Générer les datasets
docstring_data = generate_docstring_dataset()
test_data = generate_test_dataset()

# Diviser en train et eval (80/20)
def split_dataset(dataset, train_ratio=0.8):
    random.shuffle(dataset)
    split_idx = int(len(dataset) * train_ratio)
    return dataset[:split_idx], dataset[split_idx:]

docstring_train, docstring_eval = split_dataset(docstring_data)
test_train, test_eval = split_dataset(test_data)

# Sauvegarder les fichiers
def save_jsonl(data, filename):
    with open(filename, 'w') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')

save_jsonl(docstring_train, "docstring_train.jsonl")
save_jsonl(docstring_eval, "docstring_eval.jsonl")
save_jsonl(test_train, "tests_train.jsonl")
save_jsonl(test_eval, "tests_eval.jsonl")

print(f"Generated {len(docstring_train)} train and {len(docstring_eval)} eval docstring examples")
print(f"Generated {len(test_train)} train and {len(test_eval)} eval test examples")