import csv

def generate():
    with open("data/apache/logfiles.log", "r") as logfile:
        log_lines = logfile.readlines()

    with open("data/apache/data.csv", "w", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["IP Address", "Date", "Request", "Endpoint", "Status Code", "Response Size", "Referrer", "User Agent", "Time Taken"])

        for line in log_lines:
            parts = line.split(' ')
            ip_address = parts[0]
            date_time = parts[3] + ' ' + parts[4]
            request = parts[5][1:]  # İlk tırnağı kaldırıyoruz
            endpoint = parts[6]
            status_code = parts[8]
            response_size = parts[9]
            referrer = parts[10][1:-1]  # Tırnak işaretlerini kaldırıyoruz
            user_agent = ' '.join(parts[11:-1])[1:-1]  # Tırnak işaretlerini kaldırıyoruz
            time_taken = parts[-1].strip()

            csv_writer.writerow([ip_address, date_time, request, endpoint, status_code, response_size, referrer, user_agent, time_taken])

    print("Log dosyası başarıyla CSV formatına dönüştürüldü!")
