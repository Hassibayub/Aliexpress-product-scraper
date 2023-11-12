from src.ali_express import AliexpressProductScraper


def main():
    result = AliexpressProductScraper('1005006201952621', 10)
    print(result)


if __name__ == '__main__':
    main()