import sys
import os
import pymupdf # instal menggunakan file whl dari https://pypi.org/project/PyMuPDF/#files
import re
import glob

def convert_pdf_to_images(pdf_path, output_dir=None):
    try:
        if output_dir is None:
            output_dir = os.path.dirname(pdf_path)
        
        os.makedirs(output_dir, exist_ok=True)
        
        # ambil nama file pdf dan ekstrak nomor buku
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        
        # ekstrak nomor buku jika nama file mengikuti pola seperti "book 1", "book 2", dll
        book_match = re.search(r'[Bb]ook\s*(\d+)', pdf_name)
        if book_match:
            book_number = book_match.group(1)
            prefix = f"Book{book_number}"
        else:
            prefix = pdf_name
        
        doc = pymupdf.open(pdf_path)
        
        # daftar untuk menyimpan path gambar yang dihasilkan
        image_paths = []
        
        for page in doc:
            page_num = page.number + 1
            
            # buat nama file gambar keluaran
            image_path = os.path.join(output_dir, f"{prefix}_page_{page_num}.png")
            
            # render halaman ke gambar
            pix = page.get_pixmap()
            
            # simpan gambar
            pix.save(image_path)
            
            image_paths.append(image_path)
            
        print(f"berhasil mengonversi pdf ke {len(image_paths)} gambar")
        return image_paths
    
    except Exception as e:
        print(f"error saat mengonversi pdf ke gambar: {str(e)}")
        return []

def process_pdf_directory(pdf_dir, output_dir=None):
    if not os.path.isdir(pdf_dir):
        print(f"error: {pdf_dir} bukan direktori yang valid")
        return 0
        
    if output_dir is None:
        output_dir = os.path.join(pdf_dir, "converted_images")
        os.makedirs(output_dir, exist_ok=True)
    
    # ambil semua file pdf dalam direktori
    pdf_files = glob.glob(os.path.join(pdf_dir, "*.pdf"))
    
    if not pdf_files:
        print(f"tidak ada file pdf ditemukan di {pdf_dir}")
        return 0
    
    print(f"ditemukan {len(pdf_files)} file pdf untuk diproses")
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"memproses {i}/{len(pdf_files)}: {os.path.basename(pdf_file)}")
        convert_pdf_to_images(pdf_file, output_dir)
    
    return len(pdf_files)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("penggunaan:")
        print("  satu file: python converttoimg.py path_ke_pdf [direktori_output]")
        print("  semua file dalam direktori: python converttoimg.py --directory path_ke_direktori [direktori_output]")
        sys.exit(1)
    
    # periksa apakah memproses direktori
    if sys.argv[1] == "--directory":
        if len(sys.argv) < 3:
            print("error: path direktori diperlukan dengan opsi --directory")
            sys.exit(1)
        
        pdf_dir = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else None
        
        num_processed = process_pdf_directory(pdf_dir, output_dir)
        print(f"selesai memproses {num_processed} file pdf")
    
    else:
        pdf_path = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else None
        convert_pdf_to_images(pdf_path, output_dir)
