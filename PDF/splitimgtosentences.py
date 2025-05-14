import cv2
import numpy as np
import os

def split_image_on_white_lines(image_path, min_gap_height=5, intensity_threshold=150):
    # baca gambar dalam rgb dan ubah ke grayscale
    img_rgb = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if img_rgb is None:
        raise FileNotFoundError(f"gambar tidak ditemukan di {image_path}")
    
    # ubah ke grayscale untuk mendeteksi garis putih
    img = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    height, width = img.shape
    
    # profil proyeksi horizontal
    horizontal_projection = np.sum(img < intensity_threshold, axis=1)
    
    # cari jarak putih dengan tinggi minimum
    in_gap = False
    gap_start = 0
    split_points = []
    
    for y in range(height):
        if horizontal_projection[y] == 0:
            if not in_gap:
                gap_start = y
                in_gap = True
        else:
            if in_gap:
                gap_height = y - gap_start
                if gap_height >= min_gap_height:
                    split_points.append((gap_start, y))
                in_gap = False
    
    # tangani jika gambar berakhir dengan spasi putih
    if in_gap:
        gap_height = height - gap_start
        if gap_height >= min_gap_height:
            split_points.append((gap_start, height))

    # gabungkan dan buat wilayah potong
    split_regions = []
    prev_end = 0
    for (start, end) in split_points:
        if start > prev_end:
            split_regions.append((prev_end, start))
        prev_end = end
    
    # tambah wilayah terakhir
    if prev_end < height:
        split_regions.append((prev_end, height))

    # ekstrak potongan dari gambar rgb
    images = []
    for (start, end) in split_regions:
        if end - start > 1:
            images.append(img_rgb[start:end, :])
    
    return images

if __name__ == '__main__':
    img_folder = 'imgblur'
    output_folder = 'output'
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(img_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            image_path = os.path.join(img_folder, filename)
            try:
                split_images = split_image_on_white_lines(image_path)
                for i, img in enumerate(split_images):
                    out_path = os.path.join(output_folder, 
                                            f"{os.path.splitext(filename)[0]}_{i:03d}.png")
                    cv2.imwrite(out_path, img)
                print(f"{len(split_images)} gambar disimpan untuk {filename}.")
            except FileNotFoundError as e:
                print(e)
            except Exception as e:
                print(f"terjadi kesalahan pada {filename}: {e}")
