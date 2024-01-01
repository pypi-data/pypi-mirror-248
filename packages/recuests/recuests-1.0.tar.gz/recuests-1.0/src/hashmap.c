#include <stdlib.h>
#include <string.h>

#include "hashmap.h"

#define HASHMAP_DEFAULT_CAPACITY 20
#define HASHMAP_MAX_LOAD 0.75f
#define HASHMAP_RESIZE_FACTOR 2

struct bucket
{
	struct bucket* next;
	
	const void* key;
	size_t ksize;
	uint32_t hash;
	uintptr_t value;
};

struct hashmap
{
	struct bucket* buckets;
	int capacity;
	int count;

	struct bucket* first;
	
	struct bucket* last;
};

hashmap* hashmap_create(void)
{
	hashmap* m = malloc(sizeof(hashmap));
	if (m == NULL)
	{
		return NULL;
	}

	m->capacity = HASHMAP_DEFAULT_CAPACITY;
	m->count = 0;

	m->buckets = calloc(HASHMAP_DEFAULT_CAPACITY, sizeof(struct bucket));
	m->first = NULL;

	m->last = (struct bucket*)&m->first;
	return m;
}

void hashmap_free(hashmap* m)
{
	free(m->buckets);
	free(m);
}


static struct bucket* resize_entry(hashmap* m, struct bucket* old_entry)
{
	uint32_t index = old_entry->hash % m->capacity;
	for (;;)
	{
		struct bucket* entry = &m->buckets[index];

		if (entry->key == NULL)
		{
			*entry = *old_entry; 
			return entry;
		}

		index = (index + 1) % m->capacity;
	}
}

static void hashmap_resize(hashmap* m)
{
	struct bucket* old_buckets = m->buckets;

	m->capacity *= HASHMAP_RESIZE_FACTOR;
	
	m->buckets = calloc(m->capacity, sizeof(struct bucket));
	
	m->last = (struct bucket*)&m->first;
	
	do
	{
		m->last->next = resize_entry(m, m->last->next);
		m->last = m->last->next;
	} while (m->last->next != NULL);

	free(old_buckets);
}

#define HASHMAP_HASH_INIT 2166136261u


static inline uint32_t hash_data(const unsigned char* data, size_t size)
{
	size_t nblocks = size / 8;
	uint64_t hash = HASHMAP_HASH_INIT;
	for (size_t i = 0; i < nblocks; ++i)
	{
		hash ^= (uint64_t)data[0] << 0 | (uint64_t)data[1] << 8 |
			 (uint64_t)data[2] << 16 | (uint64_t)data[3] << 24 |
			 (uint64_t)data[4] << 32 | (uint64_t)data[5] << 40 |
			 (uint64_t)data[6] << 48 | (uint64_t)data[7] << 56;
		hash *= 0xbf58476d1ce4e5b9;
		data += 8;
	}

	uint64_t last = size & 0xff;
	switch (size % 8)
	{
	case 7:
		last |= (uint64_t)data[6] << 56;
	case 6:
		last |= (uint64_t)data[5] << 48;
	case 5:
		last |= (uint64_t)data[4] << 40;
	case 4:
		last |= (uint64_t)data[3] << 32;
	case 3:
		last |= (uint64_t)data[2] << 24;
	case 2:
		last |= (uint64_t)data[1] << 16;
	case 1:
		last |= (uint64_t)data[0] << 8;
		hash ^= last;
		hash *= 0xd6e8feb86659fd93;
	}

	return (uint32_t)(hash ^ hash >> 32);
}

static struct bucket* find_entry(hashmap* m, const void* key, size_t ksize, uint32_t hash)
{
	uint32_t index = hash % m->capacity;

	for (;;)
	{
		struct bucket* entry = &m->buckets[index];
		
		if (entry->key == NULL ||
			(entry->ksize == ksize &&
			 entry->hash == hash &&
			 memcmp(entry->key, key, ksize) == 0))
		{
			return entry;
		}

		index = (index + 1) % m->capacity;
	}
}

void hashmap_set(hashmap* m, const void* key, size_t ksize, uintptr_t val)
{
	if (m->count + 1 > HASHMAP_MAX_LOAD * m->capacity)
		hashmap_resize(m);

	uint32_t hash = hash_data(key, ksize);
	struct bucket* entry = find_entry(m, key, ksize, hash);
	if (entry->key == NULL)
	{
		m->last->next = entry;
		m->last = entry;
		entry->next = NULL;

		++m->count;

		entry->key = key;
		entry->ksize = ksize;
		entry->hash = hash;
	}
	entry->value = val;
}

bool hashmap_get_set(hashmap* m, const void* key, size_t ksize, uintptr_t* out_in)
{
	if (m->count + 1 > HASHMAP_MAX_LOAD * m->capacity)
		hashmap_resize(m);

	uint32_t hash = hash_data(key, ksize);
	struct bucket* entry = find_entry(m, key, ksize, hash);
	if (entry->key == NULL)
	{
		m->last->next = entry;
		m->last = entry;
		entry->next = NULL;

		++m->count;

		entry->value = *out_in;
		entry->key = key;
		entry->ksize = ksize;
		entry->hash = hash;

		return false;
	}
	*out_in = entry->value;
	return true;
}

void hashmap_set_free(hashmap* m, const void* key, size_t ksize, uintptr_t val, hashmap_callback c, void* usr)
{
	if (m->count + 1 > HASHMAP_MAX_LOAD * m->capacity)
		hashmap_resize(m);

	uint32_t hash = hash_data(key, ksize);
	struct bucket *entry = find_entry(m, key, ksize, hash);
	if (entry->key == NULL)
	{
		m->last->next = entry;
		m->last = entry;
		entry->next = NULL;

		++m->count;

		entry->key = key;
		entry->ksize = ksize;
		entry->hash = hash;
		entry->value = val;
		
		return;
	}
	
	c((void*)entry->key, ksize, entry->value, usr);

	entry->key = key;
	entry->value = val;
}

bool hashmap_get(hashmap* m, const void* key, size_t ksize, uintptr_t* out_val)
{
	uint32_t hash = hash_data(key, ksize);
	struct bucket* entry = find_entry(m, key, ksize, hash);
	
	*out_val = entry->value;

	return entry->key != NULL;
}

int hashmap_size(hashmap* m)
{
	return m->count;
}

void hashmap_iterate(hashmap* m, hashmap_callback c, void* user_ptr)
{
	struct bucket* current = m->first;
	
	while (current != NULL)
	{
		c((void*)current->key, current->ksize, current->value, user_ptr);
		current = current->next;
	}
}

