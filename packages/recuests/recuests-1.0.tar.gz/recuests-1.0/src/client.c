#include <curl/curl.h>
#include <string.h>
#include <stdlib.h>

#include "client.h"
#include "callback.h"

Response RequestGET(const char* url, HTTPHeader* headers) {
    hashmap* m = hashmap_create();
    Response res = { NULL, 0, m, 400 };


    CURL* curl = curl_easy_init();
    if (curl) {
        CURLcode ccode;
        curl_easy_setopt(curl, CURLOPT_URL, url);

        curl_easy_setopt(curl, CURLOPT_HEADERFUNCTION, HeaderCallback);
        curl_easy_setopt(curl, CURLOPT_HEADERDATA, &res);

        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, BodyCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &res);

        curl_easy_setopt(curl, CURLOPT_USERAGENT, "recuests/0.1");

        struct curl_slist* cheaders = NULL;

        if (headers != NULL) {
            size_t nsize =  sizeof(headers) / sizeof(headers[0]);
            nsize = nsize == 0? 1 : nsize;
            for (size_t i = 0; i < nsize; i++) {
                char* header = malloc(strlen(headers[i].key) + strlen(headers[i].value) + 3);
                sprintf(header, "%s: %s", headers[i].key, headers[i].value);
                cheaders = curl_slist_append(cheaders, header);
                free(header);
            }

            curl_easy_setopt(curl, CURLOPT_HTTPHEADER, cheaders);
        }

        ccode = curl_easy_perform(curl);

        if (ccode != CURLE_OK)
            fprintf(stderr, "Error: Request failed: %s\n", curl_easy_strerror(ccode));
        else
            curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &res.status);

        if (cheaders != NULL)
            curl_slist_free_all(cheaders);

        curl_easy_cleanup(curl);
    } else {
        fprintf(stderr, "Error: Request failed.\n");
    }
    
    return res;
}

Response RequestPOST(const char* url, HTTPHeader* headers, const char* postData) {
    hashmap* m = hashmap_create();
    Response res = { NULL, 0, m, 400 };


    CURL* curl = curl_easy_init();
    if (curl) {
        CURLcode ccode;
        curl_easy_setopt(curl, CURLOPT_URL, url);

        curl_easy_setopt(curl, CURLOPT_POST, 1L);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, postData);

        curl_easy_setopt(curl, CURLOPT_HEADERFUNCTION, HeaderCallback);
        curl_easy_setopt(curl, CURLOPT_HEADERDATA, &res);

        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, BodyCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &res);

        curl_easy_setopt(curl, CURLOPT_USERAGENT, "recuests/0.1");

        struct curl_slist* cheaders = NULL;

        if (headers != NULL) {
            size_t nsize =  sizeof(headers) / sizeof(headers[0]);
            nsize = nsize == 0? 1 : nsize;
            for (size_t i = 0; i < nsize; i++) {
                char* header = malloc(strlen(headers[i].key) + strlen(headers[i].value) + 3);
                sprintf(header, "%s: %s", headers[i].key, headers[i].value);
                cheaders = curl_slist_append(cheaders, header);
                free(header);
            }

            curl_easy_setopt(curl, CURLOPT_HTTPHEADER, cheaders);
        }

        ccode = curl_easy_perform(curl);

        if (ccode != CURLE_OK)
            fprintf(stderr, "Error: Request failed: %s\n", curl_easy_strerror(ccode));
        else
            curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &res.status);

        if (cheaders != NULL)
            curl_slist_free_all(cheaders);

        curl_easy_cleanup(curl);
    } else {
        fprintf(stderr, "Error: Request failed.\n");
    }
    
    return res;
}

Response RequestPUT(const char* url, HTTPHeader* headers, const char* postData) {
    hashmap* m = hashmap_create();
    Response res = { NULL, 0, m, 400 };


    CURL* curl = curl_easy_init();
    if (curl) {
        CURLcode ccode;
        curl_easy_setopt(curl, CURLOPT_URL, url);

        curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "PUT");

        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, postData);

        curl_easy_setopt(curl, CURLOPT_HEADERFUNCTION, HeaderCallback);
        curl_easy_setopt(curl, CURLOPT_HEADERDATA, &res);

        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, BodyCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &res);

        curl_easy_setopt(curl, CURLOPT_USERAGENT, "recuests/0.1");

        struct curl_slist* cheaders = NULL;

        if (headers != NULL) {
            size_t nsize =  sizeof(headers) / sizeof(headers[0]);
            nsize = nsize == 0? 1 : nsize;
            for (size_t i = 0; i < nsize; i++) {
                char* header = malloc(strlen(headers[i].key) + strlen(headers[i].value) + 3);
                sprintf(header, "%s: %s", headers[i].key, headers[i].value);
                cheaders = curl_slist_append(cheaders, header);
                free(header);
            }

            curl_easy_setopt(curl, CURLOPT_HTTPHEADER, cheaders);
        }

        ccode = curl_easy_perform(curl);

        if (ccode != CURLE_OK)
            fprintf(stderr, "Error: Request failed: %s\n", curl_easy_strerror(ccode));
        else
            curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &res.status);

        if (cheaders != NULL)
            curl_slist_free_all(cheaders);

        curl_easy_cleanup(curl);
    } else {
        fprintf(stderr, "Error: Request failed.\n");
    }
    
    return res;
}

Response RequestDELETE(const char* url, HTTPHeader* headers) {
    hashmap* m = hashmap_create();
    Response res = { NULL, 0, m, 400 };


    CURL* curl = curl_easy_init();
    if (curl) {
        CURLcode ccode;
        curl_easy_setopt(curl, CURLOPT_URL, url);

        curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "DELETE");

        curl_easy_setopt(curl, CURLOPT_HEADERFUNCTION, HeaderCallback);
        curl_easy_setopt(curl, CURLOPT_HEADERDATA, &res);

        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, BodyCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &res);

        curl_easy_setopt(curl, CURLOPT_USERAGENT, "recuests/0.1");

        struct curl_slist* cheaders = NULL;

        if (headers != NULL) {
            size_t nsize =  sizeof(headers) / sizeof(headers[0]);
            nsize = nsize == 0? 1 : nsize;
            for (size_t i = 0; i < nsize; i++) {
                char* header = malloc(strlen(headers[i].key) + strlen(headers[i].value) + 3);
                sprintf(header, "%s: %s", headers[i].key, headers[i].value);
                cheaders = curl_slist_append(cheaders, header);
                free(header);
            }

            curl_easy_setopt(curl, CURLOPT_HTTPHEADER, cheaders);
        }

        ccode = curl_easy_perform(curl);

        if (ccode != CURLE_OK)
            fprintf(stderr, "Error: Request failed: %s\n", curl_easy_strerror(ccode));
        else
            curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &res.status);

        if (cheaders != NULL)
            curl_slist_free_all(cheaders);

        curl_easy_cleanup(curl);
    } else {
        fprintf(stderr, "Error: Request failed.\n");
    }
    
    return res;
}

void FreeResponse(Response* res) {
    free(res->body);
    hashmap_free(res->headers);
}

char* GetResHeader(Response* res, const char* key) {
    uintptr_t val;
    bool b = hashmap_get(res->headers, key, strlen(key), &val);
    if (b)
        return (char*)val;
    
    return NULL;
}