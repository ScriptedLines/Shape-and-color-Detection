import cv2 as cv
import numpy as np
import webcolors
import math

COLOR_NAMES = {
    'aliceblue': '#F0F8FF',
    'antiquewhite': '#FAEBD7',
    'aqua': '#00FFFF',
    'aquamarine': '#7FFFD4',
    'azure': '#F0FFFF',
    'beige': '#F5F5DC',
    'bisque': '#FFE4C4',
    'black': '#000000',
    'blanchedalmond': '#FFEBCD',
    'blue': '#0000FF',
    'blueviolet': '#8A2BE2',
    'brown': '#A52A2A',
    'burlywood': '#DEB887',
    'cadetblue': '#5F9CAC',
    'chartreuse': '#7FFF00',
    'chocolate': '#D2691E',
    'coral': '#FF7F50',
    'cornflowerblue': '#6495ED',
    'cornsilk': '#FFF8DC',
    'crimson': '#DC143C',
    'cyan': '#00FFFF',
    'darkblue': '#00008B',
    'darkcyan': '#008B8B',
    'darkgoldenrod': '#B8860B',
    'darkgray': '#A9A9A9',
    'darkgreen': '#006400',
    'darkgrey': '#A9A9A9',
    'darkkhaki': '#BDB76B',
    'darkmagenta': '#8B008B',
    'darkolivegreen': '#556B2F',
    'darkorange': '#FF8C00',
    'darkorchid': '#9932CC',
    'darkred': '#8B0000',
    'darksalmon': '#E9967A',
    'darkseagreen': '#8FBC8F',
    'darkslateblue': '#483D8B',
    'darkslategray': '#2F4F4F',
    'darkturquoise': '#00CED1',
    'darkviolet': '#9400D3',
    'deeppink': '#FF1493',
    'deepskyblue': '#00BFFF',
    'dimgray': '#696969',
    'dodgerblue': '#1E90FF',
    'firebrick': '#B22222',
    'floralwhite': '#FFFAF0',
    'forestgreen': '#228B22',
    'fuchsia': '#FF00FF',
    'gainsboro': '#DCDCDC',
    'ghostwhite': '#F8F8FF',
    'gold': '#FFD700',
    'goldenrod': '#DAA520',
    'gray': '#808080',
    'green': '#008000',
    'greenyellow': '#ADFF2F',
    'honeydew': '#F0FFF0',
    'hotpink': '#FF69B4',
    'indianred': '#CD5C5C',
    'indigo': '#4B0082',
    'ivory': '#FFFFF0',
    'khaki': '#F0E68C',
    'lavender': '#E6E6FA',
    'lavenderblush': '#FFF0F5',
    'lawngreen': '#7CFC00',
    'lemonchiffon': '#FFFACD',
    'lightblue': '#ADD8E6',
    'lightcoral': '#F08080',
    'lightcyan': '#E0FFFF',
    'lightgoldenrodyellow': '#FAFAD2',
    'lightgray': '#D3D3D3',
    'lightgreen': '#90EE90',
    'lightpink': '#FFB6C1',
    'lightsalmon': '#FFA07A',
    'lightseagreen': '#20B2AA',
    'lightskyblue': '#87CEFA',
    'lightslategray': '#778899',
    'lightsteelblue': '#B0C4DE',
    'lightyellow': '#FFFFE0',
    'lime': '#00FF00',
    'limegreen': '#32CD32',
    'linen': '#FAF0E6',
    'magenta': '#FF00FF',
    'maroon': '#800000',
    'mediumaquamarine': '#66CDAA',
    'mediumblue': '#0000CD',
    'mediumorchid': '#BA55D3',
    'mediumpurple': '#9370DB',
    'mediumseagreen': '#3CB371',
    'mediumslateblue': '#7B68EE',
    'mediumspringgreen': '#00FA9A',
    'mediumturquoise': '#48D1CC',
    'mediumvioletred': '#C71585',
    'midnightblue': '#191970',
    'mintcream': '#F5FFFA',
    'mistyrose': '#FFE4E1',
    'moccasin': '#FFE4B5',
    'navajowhite': '#FFDEAD',
    'navy': '#000080',
    'oldlace': '#FDF5E6',
    'olive': '#808000',
    'olivedrab': '#6B8E23',
    'orange': '#FFA500',
    'orangered': '#FF4500',
    'orchid': '#DA70D6',
    'palegoldenrod': '#EEE8AA',
    'palegreen': '#98FB98',
    'paleturquoise': '#AFEEEE',
    'palevioletred': '#D87093',
    'papayawhip': '#FFEFD5',
    'peachpuff': '#FFDAB9',
    'peru': '#CD853F',
    'pink': '#FFC0CB',
    'plum': '#DDA0DD',
    'powderblue': '#B0E0E6',
    'purple': '#800080',
    'red': '#FF0000',
    'rosybrown': '#BC8F8F',
    'royalblue': '#4169E1',
    'saddlebrown': '#8B4513',
    'salmon': '#FA8072',
    'sandybrown': '#F4A460',
    'seagreen': '#2E8B57',
    'seashell': '#FFF5EE',
    'sienna': '#A0522D',
    'silver': '#C0C0C0',
    'skyblue': '#87CEEB',
    'slateblue': '#6A5ACD',
    'slategray': '#708090',
    'snow': '#FFFAFA',
    'springgreen': '#00FF7F',
    'steelblue': '#4682B4',
    'tan': '#D2B48C',
    'teal': '#008080',
    'thistle': '#D8BFD8',
    'tomato': '#FF6347',
    'turquoise': '#40E0D0',
    'violet': '#EE82EE',
    'wheat': '#F5DEB3',
    'white': '#FFFFFF',
    'whitesmoke': '#F5F5F5',
    'yellow': '#FFFF00',
    'yellowgreen': '#9ACD32'
}


def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def rgb_distance(rgb1, rgb2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)))

def closest_color(requested_color):
    min_colors = {}
    for name, hex_value in COLOR_NAMES.items():
        r_c, g_c, b_c = hex_to_rgb(hex_value)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]

def get_color_name(rgb_tuple):
    hex_value = '#{:02x}{:02x}{:02x}'.format(*rgb_tuple)
    try:
        # Use webcolors to find the exact color name if possible
        return webcolors.hex_to_name(hex_value)
    except ValueError:
        # If exact match not found, find the closest color
        return closest_color(rgb_tuple)


mine=cv.imread("D:\\Python Projects\\5.png")

minegray=cv.cvtColor(mine,cv.COLOR_BGR2GRAY)



_,countour=cv.threshold(minegray,235,250,cv.THRESH_BINARY)


counter,hie=cv.findContours(countour,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)

cv.drawContours(mine,counter,-1,(0,150,0),4)


for i, cont in enumerate(counter):
    if i==0:
        continue

    mask = np.zeros_like(minegray)
    cv.drawContours(mask, [cont], -1, 255, thickness=cv.FILLED)
    masked_image = cv.bitwise_and(mine, mine, mask=mask)
    mean_color = cv.mean(mine, mask=mask)[:3]
  
    col=[]
    for i in mean_color[::-1]:
        col.append(int(i))


    coltup=tuple(col)
    colname=get_color_name(coltup)
    
    


    area = cv.contourArea(cont)
    peri=cv.arcLength(cont,True)

    circ = 4 * 3.14 * (area / (peri ** 2))

    (x,y),rad=cv.minEnclosingCircle(cont)

    newcircarea=3.14*rad*rad




    
    epsilon=0.02*cv.arcLength(cont,True)
    approx=cv.approxPolyDP(cont,epsilon,True)
    print(area)
    print(newcircarea)
    print(circ)
    print(colname)
    print(coltup)
 
    print("\n")
 



    x,y,w,h=cv.boundingRect(approx)

    x_mid=int(x+w/8)
    y_mid=int(y+h/1.5)

    coords=(x_mid,y_mid)
    color=(0,0,0)
    font=cv.FONT_HERSHEY_DUPLEX


    if len(approx) == 3:
        cv.putText(mine, f"Triangle ({colname})", coords, font, 0.5, color, 1)
    elif len(approx) == 4:
        cv.putText(mine, f"Square or Rectangle ({colname})", coords, font, 0.5, color, 1)
    elif len(approx) == 5:
        cv.putText(mine, f"Pentagon ({colname})", coords, font, 0.5, color, 1)
    elif len(approx) == 6:
        cv.putText(mine, f"Hexagon ({colname})", coords, font, 0.5, color, 1)
    elif len(approx) == 7:
        cv.putText(mine, f"Heptagon ({colname})", coords, font, 0.5, color, 1)
    elif len(approx) == 8:
        if area - newcircarea > -500 and area - newcircarea < 500:
            cv.putText(mine, f"Circle ({colname})", coords, font, 0.5, color, 1)
        else:
            cv.putText(mine, f"Octagon ({colname})", coords, font, 0.5, color, 1)
    elif len(approx) == 9:
        cv.putText(mine, f"Nonagon ({colname})", coords, font, 0.5, color, 1)
    elif len(approx) == 10:
        cv.putText(mine, f"Decagon ({colname})", coords, font, 0.5, color, 1)
    elif len(approx) == 11:
        cv.putText(mine, f"Hendecagon ({colname})", coords, font, 0.5, color, 1)
    else:
        cv.putText(mine, f"Sides > 11 ({colname})", coords, font, 0.5, color, 1)

cv.imshow("Shapes detected",mine)
cv.waitKey(0)
    


