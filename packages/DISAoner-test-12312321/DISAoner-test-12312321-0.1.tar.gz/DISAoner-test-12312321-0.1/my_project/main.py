#Створити проєкт калькулятор звичайний написати до нього документацію і викласти до pypi

def calc(a:int,
         b:int,
         operator:int):
    """
    Функція калькулятор

    :param a: перша змінна
    :type a: int
    :param b: друга змінна
    :type b: int
    :param operator: дія між зміннами
    :type operator: int

    :return: реультат дії між змінними
    :rtype: double
    """
    if operator == 1:
        return a+b
    if operator == 2:
        return a-b
    if operator == 3:
        return a*b
    if operator == 4:
        return a/b
    if operator == 5:
        return a**b

a = input("Введіть число а: ")
b = input("Введіть число b: ")
operator = input(f"""Введіть оператор
1 +
2 -
3 *
4 /
5 **""")

if (a.isdigit()
    and b.isdigit()
    and 0 < int(operator) < 6):
    print(f"result={calc(int(a),int(b),int(operator))}")



    
