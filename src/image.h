// bitmap.h

#ifndef BITMAP_H
#define BITMAP_H

typedef struct {
    int width, height;
    unsigned char* data;
} Image;

Image* create_image_buffer(int height, int width);
void set_pixel(Image* img, int x, int y, int on);
void free_image(Image* img);
int save_to_bmp(const Image* img, const char* filename);

#endif // BITMAP_H
