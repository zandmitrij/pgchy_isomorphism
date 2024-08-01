EXTENSION = pgchy_isomorphism
MODULE_big = pgchy_isomorphism
DATA = sql/pgchy_isomorphism--1.0.sql
OBJS = src/pgchy_isomorphism.o

PG_CONFIG = pg_config
PGXS := $(shell $(PG_CONFIG) --pgxs)
include $(PGXS)

CPPFLAGS += -I$(shell $(PG_CONFIG) --includedir-server) -I/usr/include/lz4
SHLIB_LINK += -llz4

install:
	$(MKDIR_P) '$(DESTDIR)$(shell $(PG_CONFIG) --pkglibdir)'
	$(INSTALL_SHLIB) pgchy_isomorphism.so '$(DESTDIR)$(shell $(PG_CONFIG) --pkglibdir)'
	$(MKDIR_P) '$(DESTDIR)$(shell $(PG_CONFIG) --sharedir)/extension'
	$(INSTALL_DATA) pgchy_isomorphism.control '$(DESTDIR)$(shell $(PG_CONFIG) --sharedir)/extension'
	$(INSTALL_DATA) sql/pgchy_isomorphism--1.0.sql '$(DESTDIR)$(shell $(PG_CONFIG) --sharedir)/extension'
