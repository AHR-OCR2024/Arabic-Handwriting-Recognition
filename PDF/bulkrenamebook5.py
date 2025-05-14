import os
import re
import shutil

def get_page_number(filename):
    # ekstrak nomor halaman dari nama file
    match = re.search(r'page\s*(\d+)', filename, re.IGNORECASE)
    return int(match.group(1)) if match else None

def rename_files():
    input_dir = 'input'
    output_dir = 'output'
    
    # buat folder output jika belum ada
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # ambil semua file dari folder input dan urutkan
    files = sorted(os.listdir(input_dir))
    current_page = None
    line_count = 0
    
    for filename in files:
        input_path = os.path.join(input_dir, filename)
        if not os.path.isfile(input_path):
            continue
            
        page_num = get_page_number(filename)
        
        # jika file ini memiliki nomor halaman
        if page_num is not None:
            current_page = page_num
            line_count = 0
        
        # lewati file jika belum ditemukan penanda halaman
        if current_page is None:
            continue
            
        _, ext = os.path.splitext(filename)
        
        # buat nama file baru
        new_name = f'Book5_page_{current_page:03d}_{line_count:03d}{ext}'
        
        # salin file ke folder output dengan nama baru
        shutil.copy2(input_path, os.path.join(output_dir, new_name))
        line_count += 1

if __name__ == '__main__':
    rename_files()
