EXTENSION = pgchy_isomorphism
MODULE_big = pgchy_isomorphism
DATA = sql/pgchy_isomorphism--1.0.sql
OBJS = src/pgchy_isomorphism.o

PG_CONFIG = pg_config
PGXS := $(shell $(PG_CONFIG) --pgxs)
include $(PGXS)

CPPFLAGS += -I$(shell $(PG_CONFIG) --includedir-server)

SHLIB_LINK += -llz4

install:
	$(MKDIR_P) '$(DESTDIR)$(pg_config --pkglibdir)'
	$(INSTALL_SHLIB) pgchy_isomorphism.so '$(DESTDIR)$(pg_config --pkglibdir)'
	$(MKDIR_P) '$(DESTDIR)$(pg_config --sharedir)/extension'
	$(INSTALL_DATA) pgchy_isomorphism.control '$(DESTDIR)$(pg_config --sharedir)/extension'
	$(INSTALL_DATA) sql/pgchy_isomorphism--1.0.sql '$(DESTDIR)$(pg_config --sharedir)/extension'
