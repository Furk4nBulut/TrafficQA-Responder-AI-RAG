import TestFileGenerator
import CSVFileGenerator


def main():
    TestFileGenerator.generate()
    print("Test dosyası oluşturuldu!")

    CSVFileGenerator.generate()
    print("Log dosyası başarıyla CSV formatına dönüştürüldü!")


if __name__ == "__main__":
    main()
