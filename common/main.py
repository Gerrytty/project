from GA import GA

if __name__ == "__main__":
    # weights and delays where we choose
    weights = [(i + 1) * 50.0 for i in range(100)]
    delays = [(i + 1) * 0.5 for i in range(10)]

    ga = GA(weights, delays)