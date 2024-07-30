EXTENSION = pgchy_isomorphism
MODULE_big = pgchy_isomorphism
OBJS = src/pgchy_isomorphism.o

PG_CONFIG = pg_config
PGXS := $(shell $(PG_CONFIG) --pgxs)
include $(PGXS)

# Добавьте директорию, содержащую заголовки LZ4, в путь включения
CPPFLAGS += -I/usr/include

# Линковка с библиотекой LZ4
SHLIB_LINK += -llz4
