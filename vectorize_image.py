from PIL import Image
import potrace
import numpy as np

def raster_to_vector(input_image_path, output_svg_path):
    """Converte uma imagem raster em um arquivo SVG vetorial."""
    # Carrega a imagem e converte para tons de cinza
    image = Image.open(input_image_path).convert('L')
    
    # Converte para array NumPy e binariza
    bitmap = np.array(image) > 128
    
    # Cria o traçado vetorial
    trace = potrace.Bitmap(bitmap).trace()
    
    # Escreve o arquivo SVG
    with open(output_svg_path, 'w') as f:
        f.write('<?xml version="1.0" standalone="no"?>\n')
        f.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n')
        f.write('<svg version="1.1" xmlns="http://www.w3.org/2000/svg">\n')
        
        for curve in trace:
            f.write('<path d="')
            f.write(f'M {curve.start_point.x} {curve.start_point.y} ')
            for segment in curve:
                if isinstance(segment, potrace.CornerSegment):
                    f.write(f'L {segment.c.x} {segment.c.y} L {segment.end_point.x} {segment.end_point.y} ')
                else:  # BezierSegment
                    f.write(f'C {segment.c1.x} {segment.c1.y} {segment.c2.x} {segment.c2.y} {segment.end_point.x} {segment.end_point.y} ')
            f.write('Z" fill="black" stroke="black" stroke-width="1"/>\n')
        
        f.write('</svg>')

if __name__ == "__main__":
    input_path = "input_image.png"
    output_path = "output_image.svg"
    raster_to_vector(input_path, output_path)
    print(f"Imagem vetorial salva em {output_path}")
