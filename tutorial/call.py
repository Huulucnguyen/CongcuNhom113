from crawl import get_list, load_url_selenium_shopee
import numpy as np
import os

lst = ['Bụng cảm giác hơi bó còn ống quần thì rộng hơn ảnh mẫu k được đẹp', 'Form đẹp', 'Quần đẹp giao hàng nhanh', 'quần vừa  nhưng ống hơi dài phải mang đi cắt màu trắng nhưng vải ko bị mỏng quá mặc ko bị lộ Đóng cúc rồi thì phần mép khóa hơi ko khít nên cho 4* thôi nhé', 'Quần lên dáng khá là xinh ạ', 'Mình cao 1m58 48kg mặc vừa size S quần chất tương đối đẹp khá mềm', 'Quần chất hơi mỏng ko đứng dáng quần lắm', 'Áo chất đẹp lắm ạ']

full_lst = []
for i in lst:
    new_lst = []
    new_lst = [i]
    full_lst.append(new_lst)
print(full_lst)