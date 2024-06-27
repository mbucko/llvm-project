#include <cstdlib>
#include <cstring>
#include <memory>
#include <string>

int main() {
  constexpr uint64_t size = 4 * 1024 * 1024 * 1024ull;
  char *heap_pointer1 = new char[size];
  char *heap_pointer2 = heap_pointer1;
  (void)heap_pointer2;
  constexpr char string_value[] = "heap_there_is_exactly_two_of_me";
  constexpr uint64_t string_size = sizeof(string_value) + 1;

  size_t size_tmp = 2 * string_size;
  void *aligned_string_ptr = heap_pointer1 + size - 2 * string_size;
  aligned_string_ptr = std::align(8, string_size, aligned_string_ptr, size_tmp);
  memset(heap_pointer1, 1, size);
  memcpy(aligned_string_ptr, string_value, string_size);

  return 0; // break here
}
