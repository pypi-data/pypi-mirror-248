#include <string.h>
#include <stdlib.h>

#include "client.h"
#include "callback.h"
#include "hashmap.h"

size_t HeaderCallback(void* contents, size_t size, size_t nmemb, void* userdata) {
    size_t totalSize = size * nmemb;
    Response *res = (Response*)userdata;
    char* header = (char*)contents;
    
    if (totalSize <= 2 || header[0] == '\r' || header[0] == '\n')
        return totalSize;

    if (header[totalSize - 2] == '\r' || header[totalSize - 2] == '\n')    
        header[totalSize - 2] = '\0';

    char* key = strtok(header, ":");
    char* val = strtok(header + strlen(key) + 2, "");

    if (key == NULL || val == NULL)
        return totalSize;

    char* hkey = strdup(key);
    char* hval = strdup(val);

    hashmap_set(res->headers, hkey, strlen(hkey), (uintptr_t)hval);

    return totalSize;
}

size_t BodyCallback(void* contents, size_t size, size_t nmemb, void* userdata) {
    Response* res = (Response*)userdata;
    size_t newSize = res->bodySize + size * nmemb;
    res->body = realloc(res->body, newSize + 1);
    if (res->body == NULL)
        return 0;

    memcpy(res->body + res->bodySize, contents, size * nmemb);
    res->body[newSize] = '\0';
    res->bodySize = newSize;

    return size * nmemb;
}