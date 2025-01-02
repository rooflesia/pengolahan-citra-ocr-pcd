def parse_location_tag(location_string):
    """
    Mengonversi string lokasi seperti <loc0176><loc0022><loc0738><loc0844>
    menjadi bounding box (x_min, y_min, x_max, y_max).
    """
    # Bersihkan string dan pisahkan menjadi elemen
    loc_tags = location_string.strip().split("><")
    loc_tags = [tag.replace("<loc", "").replace(">", "") for tag in loc_tags]
    
    # Pastikan jumlah elemen sesuai
    if len(loc_tags) == 4:
        # Konversi setiap elemen ke integer
        x_min, y_min, x_max, y_max = map(int, loc_tags)
        return x_min, y_min, x_max, y_max
    else:
        raise ValueError("Format lokasi tidak valid: Harus memiliki 4 elemen.")

# Contoh penggunaan
if __name__ == "__main__":
    location_string = "<loc0176><loc0022><loc0738><loc0844>"
    bounding_box = parse_location_tag(location_string)
    print(f"Bounding Box: {bounding_box}")
