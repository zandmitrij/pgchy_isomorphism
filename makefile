EXTENSION = pgchy_isomorphism
MODULE_big = pgchy_isomorphism
DATA = pgchy_isomorphism--1.0.sql
OBJS = src/pgchy_isomorphism.o

PG_CONFIG = pg_config
PGXS := $(shell $(PG_CONFIG) --pgxs)
include $(PGXS)

CPPFLAGS += -I$(shell $(PG_CONFIG) --includedir-server)

SHLIB_LINK += -llz4
