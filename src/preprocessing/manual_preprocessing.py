import os
from PIL import Image
import numpy as np

# def read_image(file_path):
#     """
#     Membaca gambar dalam format grayscale dan mengembalikan sebagai matriks 2D.
#     """
#     with open(file_path, 'rb') as f:
#         data = f.read()
    
#     # Read the BMP header for width and height
#     header_size = 54
#     width = int.from_bytes(data[18:22], byteorder='little')
#     height = int.from_bytes(data[22:26], byteorder='little')
    
#     # Extract pixel data
#     pixels = data[header_size:]
#     matrix =  [pixels[i * width:(i + 1) * width] for i in range(height)]
#     return matrix, width, height

# def read_image(file_path):
#     """
#     Membaca gambar BMP menggunakan Pillow dan mengembalikan matriks piksel.
#     """
#     img = Image.open(file_path).convert('L')  # Konversi ke grayscale
#     width, height = img.size
#     matrix = list(img.getdata())
#     matrix = [matrix[i * width:(i + 1) * width] for i in range(height)]
#     return matrix, width, height

# def read_image(file_path):
#     """
#     Membaca gambar BMP dengan memperhitungkan padding di setiap baris.
#     """
#     with open(file_path, 'rb') as f:
#         data = f.read()
    
#     # Read the BMP header for width and height
#     header_size = 54
#     width = int.from_bytes(data[18:22], byteorder='little')
#     height = int.from_bytes(data[22:26], byteorder='little')
    
#     # Calculate row size including padding
#     row_size = (width + 3) // 4 * 4
    
#     # Extract pixel data
#     pixels = data[header_size:]
#     matrix = []
#     for i in range(height):
#         row_start = i * row_size
#         row_end = row_start + width
#         matrix.append(list(pixels[row_start:row_end]))
#     return matrix, width, height


def read_image(file_path):
    """
    Reads a BMP image file and returns a matrix representing the image
    along with its width and height. This function is inspired by
    Image.open but is tailored for BMP files.
    """
    with open(file_path, 'rb') as f:
        data = f.read()

    # Parse BMP header
    if data[:2] != b'BM':
        raise ValueError("Not a BMP file")

    file_size = int.from_bytes(data[2:6], byteorder='little')
    pixel_data_offset = int.from_bytes(data[10:14], byteorder='little')

    # Parse DIB header
    dib_header_size = int.from_bytes(data[14:18], byteorder='little')
    width = int.from_bytes(data[18:22], byteorder='little')
    height = int.from_bytes(data[22:26], byteorder='little')
    planes = int.from_bytes(data[26:28], byteorder='little')
    bits_per_pixel = int.from_bytes(data[28:30], byteorder='little')

    if planes != 1 or dib_header_size < 40:
        raise ValueError("Unsupported BMP format")

    # Determine pixel format
    bytes_per_pixel = bits_per_pixel // 8
    if bits_per_pixel == 24:
        mode = "RGB"
    elif bits_per_pixel == 8:
        mode = "L"
    else:
        raise ValueError(f"Unsupported bits per pixel: {bits_per_pixel}")

    # Calculate row size with padding
    row_size = (width * bytes_per_pixel + 3) & ~3

    # Read pixel data
    pixel_data = data[pixel_data_offset:]
    matrix = []

    for row_index in range(height):
        row_start = row_index * row_size
        row_end = row_start + (width * bytes_per_pixel)
        row = pixel_data[row_start:row_end]

        if mode == "RGB":
            row_pixels = [(row[i + 2], row[i + 1], row[i]) for i in range(0, len(row), 3)]  # BGR to RGB
        elif mode == "L":
            row_pixels = list(row)

        matrix.append(row_pixels)

    # Flip rows vertically (BMP stores rows bottom-up)
    # matrix = matrix[::-1]

    return matrix, width, height


def matrix_to_image(matrix, width, height):
    """
    Convert the 2D grayscale matrix to an image and save/show it.
    """
    # Flatten the matrix into a single array
    flat_matrix = [pixel for row in matrix for pixel in row]
    
    # Create an image using Pillow
    image = Image.frombytes('L', (width, height), bytes(flat_matrix))
    
    # Save or display the image
    image.save("output_image.png")
    image.show()


def gaussian_blur(matrix, width, height, kernel_size=3):
    """
    Menghapus noise menggunakan Gaussian blur secara manual.
    """
    def gaussian_kernel(size):
        kernel = [[1 for _ in range(size)] for _ in range(size)]
        return [[kernel[i][j] / (size * size) for j in range(size)] for i in range(size)]
    
    kernel = gaussian_kernel(kernel_size)
    padding = kernel_size // 2
    result = [[0 for _ in range(width)] for _ in range(height)]

    for i in range(padding, height - padding):
        for j in range(padding, width - padding):
            sum_val = 0
            for ki in range(kernel_size):
                for kj in range(kernel_size):
                    sum_val += matrix[i - padding + ki][j - padding + kj] * kernel[ki][kj]
            result[i][j] = max(0, min(255, int(sum_val)))  # memastikan nilai dalam rentang 0-255

    print("Contoh nilai piksel setelah Gaussian blur:")
    for row in result[:5]:  # Cetak 5 baris pertama
        print(row[:10])  # Cetak 10 kolom pertama
    return result


def normalize_pixel_values(matrix):
    """
    Menormalkan nilai piksel agar berada dalam rentang 0–255.
    """
    flat_values = [pixel for row in matrix for pixel in row]
    min_val = min(flat_values)
    max_val = max(flat_values)

    if max_val > min_val:
        normalized_matrix = [
            [int(255 * (pixel - min_val) / (max_val - min_val)) for pixel in row]
            for row in matrix
        ]
    else:
        normalized_matrix = matrix

    return normalized_matrix


# def save_image(matrix, output_file, mode="PNG"):
#     """
#     Menyimpan matriks gambar ke dalam format PNG atau BMP.
#     """
#     # Balikkan urutan baris untuk memastikan urutan bottom-to-top
#     flipped_matrix = matrix[::-1]
    
#     # Konversi ke numpy array
#     img_array = np.array(flipped_matrix, dtype=np.uint8)
    
#     # Simpan sebagai PNG
#     if mode == "PNG":
#         img = Image.fromarray(img_array, mode="L")
#         img.save(output_file)
#         print(f"Gambar disimpan sebagai PNG: {output_file}")
    
#     # Simpan sebagai BMP
#     elif mode == "BMP":
#         img = Image.fromarray(img_array, mode="L")
#         img.save(output_file, format="BMP")
#         print(f"Gambar disimpan sebagai BMP: {output_file}")


def save_image(matrix, output_file):
    """
    Menyimpan matriks gambar ke dalam file BMP sederhana.
    """
    height = len(matrix)
    width = len(matrix[0])
    header = bytearray(54)
    header[0:2] = b'BM'
    header[2:6] = (54 + 1024 + width * height).to_bytes(4, byteorder='little')  # File size
    header[10:14] = (54 + 1024).to_bytes(4, byteorder='little')  # Offset pixel array
    header[14:18] = (40).to_bytes(4, byteorder='little')  # Header size
    header[18:22] = (width).to_bytes(4, byteorder='little')  # Image width
    header[22:26] = (height).to_bytes(4, byteorder='little')  # Image height
    header[26:28] = (1).to_bytes(2, byteorder='little')  # Planes
    header[28:30] = (8).to_bytes(2, byteorder='little')  # Bits per pixel
    header[34:38] = (width * height).to_bytes(4, byteorder='little')  # Image size

    # Buat palet grayscale
    palette = bytearray()
    for i in range(256):
        palette += bytes((i, i, i, 0))

    # Balikkan urutan baris
    flipped_matrix = matrix[::-1]

    # Buat array piksel
    pixel_array = np.array(flipped_matrix, dtype=np.uint8)

    # Simpan ke file BMP
    img = Image.fromarray(pixel_array, mode="L")
    img.save(output_file, format="BMP")
    print(f"Gambar disimpan sebagai BMP: {output_file}")
    # with open(output_file, 'wb') as f:
    #     f.write(header + palette + pixel_array)
    #     print(f"Gambar disimpan di: {output_file}")



if __name__ == "__main__":
    input_dir = "./data/processed/bmp_grayscale"
    output_dir = "./data/processed/manual_preprocessed_new"
    os.makedirs(output_dir, exist_ok=True)

    for image_file in os.listdir(input_dir):
        if image_file.endswith(".bmp"):
            input_path = os.path.join(input_dir, image_file)
            print(f"Memproses {image_file}")

            # Baca gambar
            matrix, width, height = read_image(input_path)
            
            # Gaussian blur
            blurred_matrix = gaussian_blur(matrix, width, height)

            # Normalisasi nilai piksel
            normalized_matrix = normalize_pixel_values(blurred_matrix)

            # Simpan hasil
            output_path = os.path.join(output_dir, f"preprocessed_{image_file}")
            save_image(normalized_matrix, output_path)
