INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_SIDS sids)

FIND_PATH(
    SIDS_INCLUDE_DIRS
    NAMES sids/api.h
    HINTS $ENV{SIDS_DIR}/include
        ${PC_SIDS_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    SIDS_LIBRARIES
    NAMES gnuradio-sids
    HINTS $ENV{SIDS_DIR}/lib
        ${PC_SIDS_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(SIDS DEFAULT_MSG SIDS_LIBRARIES SIDS_INCLUDE_DIRS)
MARK_AS_ADVANCED(SIDS_LIBRARIES SIDS_INCLUDE_DIRS)

