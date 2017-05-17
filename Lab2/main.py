from numpy.random import random_integers
from math import sqrt
from termcolor import colored
from random import sample, randint


from settings import M, MG, N, z, size_of_strat, number_of_strat


def avg(popul):
    summa = sum(popul)
    popul_avg = summa / N

    return summa, popul_avg


def disp(popul):
    popul_avg = avg(popul)[1]
    popul_disp = sqrt(sum((el - popul_avg) ** 2 for el in popul) / (N - 1))
    return popul_disp


def get_sample(popul, m):
    samp = sample(list(popul), m)
    return samp


def get_systematic_sample(popul, m):
    step = len(popul) // m
    return popul[randint(0, step)::step]


def get_stratified_sample(popul, m, n):         # m - кі-сть елементів у страті  n - кількість страт
    quan = len(popul) // n
    samp = []
    for i in range(n):
        samp.append(sample(list(popul[i * quan:(i + 1) * quan]), m))
    return samp


#ŷs
def y_average(samp):
    y_avg = sum(samp) / len(samp)
    return y_avg

#s**2
def y_dispersion(samp, y_avg):
    y_disp = sum((el - y_avg) ** 2 for el in samp) / (len(samp) - 1)
    return y_disp


def y_sum_estim(y_avg, n):
    return y_avg * n


def y_avg_estim_dispersion(y_disp, m, n):
    return y_disp * (1 - m / n) / m


def y_sum_estim_dispersion(y_avg_estim, n):
    return y_avg_estim * (n ** 2)


def get_avg_confidence_interval(y_avg, y_disp, m, n, z):
    return y_avg - z * sqrt(y_disp) * sqrt(1 - m / n) / m, y_avg + z * sqrt(y_disp) * sqrt(1 - m / n) / m


def get_sum_confidence_interval(y_avg, y_disp, m, n, z):
    return n * y_avg - z * sqrt(y_disp) * n * sqrt(1 - m / n) / sqrt(m),\
           n * y_avg + z * sqrt(y_disp) * n * sqrt(1 - m / n) / sqrt(m)


def get_stratum_sums(samp, k):               #Nh / nh = k
    return [sum(el) * k for el in samp]







if __name__ == '__main__':


    print('M = ', M, 'N = ', N)
    # p. A
    print('A')
    popul = random_integers(10 + M, MG + 2 * M, N)
    popul_sum, popul_avg = avg(popul)
    popul_disp = disp(popul)

    print(colored('sum = ', 'yellow'), popul_sum,)
    print(colored('popul_avg = ', 'blue'), popul_avg)
    print(colored('popul_disp = ', 'red'),  popul_disp)
    print('-' * 100)

    # p. Б
    print('Б')
    samp = get_sample(popul, M)
    y_avg = y_average(samp)
    y_disp = y_dispersion(samp, y_avg)
    y_sum = y_sum_estim(y_avg, N)
    y_avg_est_disp = y_avg_estim_dispersion(y_disp, M, N)
    y_sum_est_disp = y_sum_estim_dispersion(y_avg_est_disp, N)

    print(colored('samp = ', 'yellow'), samp, )
    print(colored('sum_sample = ', 'magenta'), y_sum)
    print(colored('y_avg = ', 'blue'), y_avg)
    print(colored('y_disp = ', 'red'), y_disp)
    print(colored('y_sum_est_disp = ', 'green'), y_sum_est_disp)
    print(colored('y_avg_est_disp = ', 'green'), y_avg_est_disp)
    print(colored('Верхній та нижній довірчі інтервали для середнього значення: ', 'red'),
          get_avg_confidence_interval(y_avg, y_disp, M, N, z))
    print(colored('Верхній та нижній довірчі інтервали для суми:', 'red'),
          get_sum_confidence_interval(y_avg, y_disp, M, N, z))
    print('-' * 100)

    # p.Г
    print('Г')
    print(colored('Систематична вибірка:', 'yellow'))
    samp = get_systematic_sample(popul, M)
    y_avg = y_average(samp)
    y_disp = y_dispersion(samp, y_avg)
    y_sum = y_sum_estim(y_avg, N)
    y_avg_est_disp = y_avg_estim_dispersion(y_disp, M, N)
    y_sum_est_disp = y_sum_estim_dispersion(y_avg_est_disp, N)

    print(colored('samp = ', 'yellow'), samp, )
    print(colored('sum_sample = ', 'magenta'), y_sum)
    print(colored('y_avg = ', 'blue'), y_avg)
    print(colored('y_disp = ', 'red'), y_disp)
    print(colored('y_sum_est_disp = ', 'green'), y_sum_est_disp)
    print(colored('y_avg_est_disp = ', 'green'), y_avg_est_disp)
    print(colored('Верхній та нижній довірчі інтервали для середнього значення: ', 'red'),
          get_avg_confidence_interval(y_avg, y_disp, M, N, z))
    print(colored('Верхній та нижній довірчі інтервали для суми:', 'red'),
          get_sum_confidence_interval(y_avg, y_disp, M, N, z))
    print('-' * 100)



    # p. D
    print('Д')
    strat_sample = get_stratified_sample(popul, size_of_strat, number_of_strat)
    quan = len(popul) // number_of_strat    #nh
    #print(strat_sample)

    k = quan / size_of_strat

    stratum_sums = get_stratum_sums(strat_sample, k)
    stratum_avgs = [el / size_of_strat for el in stratum_sums]
    stratum_dispersions = []
    for h in range(number_of_strat):
        stratum_dispersions.append(sum((strat_sample[h][i] - stratum_avgs[h]) ** 2 / (quan - 1) for i in range(size_of_strat)))
    print(colored('Оцінка вибіркової дисперсії для страт: ','magenta'),stratum_dispersions)


    sum_estimate = sum(stratum_sums)          #ŷh
    print(colored('Оцінка загальної суми для страти: ', 'blue'), stratum_sums)
    print(colored('Оцінка суми популяції при використанні стратифікованої вибірки: ', 'green'), sum_estimate)

    avg_estimate = sum_estimate / N  #ŷ'st

    print(colored('Оцінка середнього популяції при використанні стратифікованої вибірки: ', 'green'), avg_estimate)

    stratified_sum_dispersion = sum((1 - size_of_strat / quan) * stratum_dispersions[i] * (size_of_strat ** 2) / quan
                                    for i in range(number_of_strat))
    print(colored('Незміщена оцінка для дисперсії: ', 'blue'), stratified_sum_dispersion)
    print(colored('Незміщена оцінка для дисперсії / N**2 : ', 'blue'), stratified_sum_dispersion / (N ** 2))
    print(colored('Інтервал для оцінки середнього значення', 'cyan'),' (',
          (avg_estimate - z * sqrt(stratified_sum_dispersion / (N ** 2))),
          (avg_estimate + z * sqrt(stratified_sum_dispersion / (N ** 2))),') ')

    print('-' * 100)


    # p. В
    print('В')
    print('M = ', 100, 'N = ', 10000)

    popul = random_integers(10 + 100, MG + 2 * 100, 10000)
    popul_sum, popul_avg = avg(popul)
    popul_disp = disp(popul)

    print(colored('sum = ', 'yellow'), popul_sum, )
    print(colored('popul_avg = ', 'blue'), popul_avg)
    print(colored('popul_disp = ', 'red'), popul_disp)
    samp = get_sample(popul, 100)
    y_avg = y_average(samp)
    y_disp = y_dispersion(samp, y_avg)
    y_sum = y_sum_estim(y_avg, 10000)
    y_avg_est_disp = y_avg_estim_dispersion(y_disp, 100, 10000)
    y_sum_est_disp = y_sum_estim_dispersion(y_avg_est_disp, 10000)

    #print(colored('samp = ', 'yellow'), samp, )
    print(colored('sum_sample = ', 'magenta'), y_sum)
    print(colored('y_avg = ', 'blue'), y_avg)
    print(colored('y_disp = ', 'red'), y_disp)
    print(colored('y_sum_est_disp = ', 'green'), y_sum_est_disp)
    print(colored('y_avg_est_disp = ', 'green'), y_avg_est_disp)
    print(colored('Верхній та нижній довірчі інтервали для середнього значення: ', 'red'),
          get_avg_confidence_interval(y_avg, y_disp, 100, 10000, z))
    print(colored('Верхній та нижній довірчі інтервали для суми:', 'red'),
          get_sum_confidence_interval(y_avg, y_disp, 100, 10000, z))
    print('-' * 100)

    print('M = ', 1000, 'N = ', 10000)
    popul = random_integers(10 + 1000, MG + 2 * 1000, 10000)
    popul_sum, popul_avg = avg(popul)
    popul_disp = disp(popul)

    print(colored('sum = ', 'yellow'), popul_sum, )
    print(colored('popul_avg = ', 'blue'), popul_avg)
    print(colored('popul_disp = ', 'red'), popul_disp)

    samp = get_sample(popul, 1000)
    y_avg = y_average(samp)
    y_disp = y_dispersion(samp, y_avg)
    y_sum = y_sum_estim(y_avg, 10000)
    y_avg_est_disp = y_avg_estim_dispersion(y_disp, 1000, 10000)
    y_sum_est_disp = y_sum_estim_dispersion(y_avg_est_disp, 10000)

    #print(colored('samp = ', 'yellow'), samp, )
    print(colored('sum_sample = ', 'magenta'), y_sum)
    print(colored('y_avg = ', 'blue'), y_avg)
    print(colored('y_disp = ', 'red'), y_disp)
    print(colored('y_sum_est_disp = ', 'green'), y_sum_est_disp)
    print(colored('y_avg_est_disp = ', 'green'), y_avg_est_disp)
    print(colored('Верхній та нижній довірчі інтервали для середнього значення: ', 'red'),
          get_avg_confidence_interval(y_avg, y_disp, 1000, 10000, z))
    print(colored('Верхній та нижній довірчі інтервали для суми:', 'red'),
          get_sum_confidence_interval(y_avg, y_disp, 1000, 10000, z))
    print('-' * 100)

