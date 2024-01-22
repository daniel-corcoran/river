#include "image.h"
#include <stdlib.h>
#include <stdio.h>
#include <fstream>

Image* create_image_buffer(int height, int width) {
    Image* img = (Image*)malloc(sizeof(Image));
    if (!img) return NULL;

    img->width = width;
    img->height = height;
    img->data = (unsigned char*)calloc(width * height, sizeof(unsigned char));
    if (!img->data) {
        free(img);
        return NULL;
    }

    return img;
}

void set_pixel(Image* img, int x, int y, int on) {
    if (x >= 0 && x < img->width && y >= 0 && y < img->height) {
        img->data[y * img->width + x] = on ? 255 : 0;
    }
}

void free_image(Image* img) {
    if (img) {
        free(img->data);
        free(img);
    }
}

int save_to_bmp(const Image* img, const char* filename) {
    if (!img || !filename) return false;

    std::ofstream file(filename, std::ios::binary);
    if (!file.is_open()) return false;

    // BMP Header
    unsigned char bmpHeader[54] = {
        0x42, 0x4D,           // Magic identifier
        0, 0, 0, 0,           // File size (will be filled in later)
        0, 0, 0, 0,           // Reserved
        54, 0, 0, 0,          // Offset to image data
        40, 0, 0, 0,          // Header size
        0, 0, 0, 0,           // Width (will be filled in later)
        0, 0, 0, 0,           // Height (will be filled in later)
        1, 0,                 // Planes
        24, 0,                // Bits per pixel
        0, 0, 0, 0,           // Compression (none)
        0, 0, 0, 0,           // Image size (can be zero for uncompressed)
        0, 0, 0, 0,           // X pixels per meter
        0, 0, 0, 0,           // Y pixels per meter
        0, 0, 0, 0,           // Total colors
        0, 0, 0, 0            // Important colors
    };

    // Filling in the width and height in the header
    *(int*)&bmpHeader[18] = img->width;
    *(int*)&bmpHeader[22] = img->height;

    // Calculating the padding size
    int paddingAmount = (4 - (img->width * 3) % 4) % 4;

    // Calculating the total size of the image data (including padding)
    int dataSize = (img->width * 3 + paddingAmount) * img->height;

    // Filling in the file size in the header
    *(int*)&bmpHeader[2] = 54 + dataSize;

    // Writing the BMP Header
    file.write(reinterpret_cast<char*>(bmpHeader), sizeof(bmpHeader));

    // Writing the image data
    unsigned char padding[3] = {0, 0, 0};
    for (int y = img->height - 1; y >= 0; --y) {
        for (int x = 0; x < img->width; ++x) {
            unsigned char pixel[3] = {
                img->data[y * img->width + x], // Blue
                img->data[y * img->width + x], // Green
                img->data[y * img->width + x]  // Red
            };
            file.write(reinterpret_cast<char*>(pixel), 3);
        }
        file.write(reinterpret_cast<char*>(padding), paddingAmount);
    }

    return true;
}