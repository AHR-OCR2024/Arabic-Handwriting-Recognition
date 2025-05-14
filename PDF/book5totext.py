import os
import json
import re
import requests

# NOTE KALAU DI JSON NYA SUDAH ADA, DIA BAKAL SKIP. 
# KALAU MAU ULANG, HAPUS FILE JSON NYA 

# folder gambar yang ingin diproses
image_directory = r"C:\Users\USER\Documents\work\Arabic-Handwriting-Recognition\PDF\book5_Split"

# endpoint api
api_url = "https://4917-116-90-183-161.ngrok-free.app/upload-image"

# hasil disimpan sebagai file json
output_file = r"C:\Users\USER\Documents\work\Arabic-Handwriting-Recognition\PDF\kuning.json"

# regex untuk mengambil informasi buku, halaman, dan baris dari nama file
filename_pattern = r"(\w+)_page_(\d+)_(\d+)"

def extract_book_page_line(filename):
    match = re.match(filename_pattern, filename)
    if match:
        book = match.group(1)
        page = match.group(2)
        line = match.group(3)
        return book, page, line
    return None, None, None

def process_image(image_path):
    try:
        filename = os.path.splitext(os.path.basename(image_path))[0]
        book, page, line = extract_book_page_line(filename)
        
        if not book or not page or not line:
            print(f"tidak dapat mengambil informasi dari nama file: {filename}")
            return None
        
        with open(image_path, 'rb') as img_file:
            image_data = img_file.read()
        
        # buat data form sesuai komponen react yang ada
        files = {'image': (os.path.basename(image_path), image_data, 'image/png')}
        data = {
            'model': 'model1',
            'geometricUnwrapping': 'true',
            'illuminationRectifying': 'true'
        }
        
        print(f"mengirim {filename} ke api...")
        response = requests.post(api_url, data=data, files=files)
        
        if response.status_code == 200:
            result = response.json()
            
            # gabungkan label menjadi satu string
            if 'labels' in result:
                combined_text = ' '.join(result['labels'])
                
                return {
                    'file': book,
                    'page': page,
                    'line': line,
                    'text': combined_text
                }
            else:
                print(f"tidak ada label dalam respons untuk {filename}")
                return None
        else:
            print(f"gagal memproses {filename}: {response.status_code}")
            print(f"respons: {response.text}")
            return None
    
    except Exception as e:
        print(f"terjadi kesalahan saat memproses {image_path}: {str(e)}")
        return None

def main():
    results = []
    # cek apakah file hasil sudah ada dan muat data sebelumnya
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                results = json.load(f)
        except json.JSONDecodeError:
            print(f"gagal membaca file hasil yang ada. mulai dari awal.")
    
    for filename in os.listdir(image_directory):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            image_path = os.path.join(image_directory, filename)
            
            filename_no_ext = os.path.splitext(filename)[0]
            book, page, line = extract_book_page_line(filename_no_ext)
            
            # lewati jika sudah diproses sebelumnya
            if any(r.get('file') == book and r.get('page') == page and r.get('line') == line for r in results):
                print(f"melewati {filename} karena sudah diproses")
                continue
                
            result = process_image(image_path)
            if result:
                results.append(result)
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                print(f"berhasil memproses {filename}")
    
    print(f"selesai memproses semua gambar. hasil disimpan di {output_file}")

if __name__ == "__main__":
    main()
