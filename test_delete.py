def is_subset(arr1, arr2):
    d = make_dict(arr1)
    print(d.keys())
    for i in arr2:
        try:
            if d[i] and d[i] > 0:
                d[i] = d[i]-1
            else:
                return False
        except KeyError:
            return False
    return True


def make_dict(arr1):
    tmp_dict = {}
    for i in arr1:
        if i in tmp_dict:
            tmp_dict[i] = tmp_dict[i]+1
        else:
            tmp_dict[i] = 1
    return tmp_dict


def main():
    arr1 = [1, 2, 3, 4, 5]
    arr2 = [4, 5, 2, 19]
    answer = is_subset(arr1, arr2)
    print('Your answer is %s' % str(answer))

    sort_arr1 = sorted(arr1, key=lambda x: x, reverse=True)
    print(list(set(sort_arr1)))

if __name__ == '__main__':
    main()
