def mean(array):
    return sum(array) / len(array)

def median(array):
    array.sort()
    if len(array) % 2 == 0:
        return (array[len(array) // 2] + array[len(array) // 2 - 1]) / 2
    else:
        return array[len(array) // 2]

def mode(array):
    array.sort()
    count = {}
    for i in array:
        if i in count:
            count[i] += 1
        else:
            count[i] = 1
    return max(count, key=count.get)

def range(array):
    array.sort()
    return array[len(array) - 1] - array[0]

def variance(array):
    mean_value = mean(array)
    return sum((x - mean_value) ** 2 for x in array) / len(array)

def standard_deviation(array):
    return variance(array) ** 0.5

def covariance(array1, array2):
    mean1 = mean(array1)
    mean2 = mean(array2)
    return sum((x - mean1) * (y - mean2) for x, y in zip(array1, array2)) / len(array1)

def correlation(array1, array2):
    return covariance(array1, array2) / (standard_deviation(array1) * standard_deviation(array2))

def linear_regression(array1, array2):
    mean1 = mean(array1)
    mean2 = mean(array2)
    cov = covariance(array1, array2)
    var1 = variance(array1)
    var2 = variance(array2)
    return cov / (var1 * var2)