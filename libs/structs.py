class total_file:

    def __init__(file_tftp, code):
        file_tftp.__code = code
        file_tftp.__name = None
        file_tftp.__nbloc = None
        file_tftp.__coderr = None
        file_tftp.__mode = None
        file_tftp.__dades = None
        file_tftp.__error = None

    # Getters
    def getCode(file_tftp):
        return file_tftp.__code

    def getName(file_tftp):
        return file_tftp.__name

    def getNbloc(file_tftp):
        return file_tftp.__nbloc

    def getCoderr(file_tftp):
        return file_tftp.__coderr

    def getMode(file_tftp):
        return file_tftp.__mode

    def getDades(file_tftp):
        return file_tftp.__dades

    def getError(file_tftp):
        return file_tftp.__error

    # Setters
    def setCode(file_tftp, code):
        file_tftp.__code = code

    def setName(file_tftp, name):
        file_tftp.__name = name

    def setNbloc(file_tftp, nbloc):
        file_tftp.__nbloc = nbloc

    def setCoderr(file_tftp, coderr):
        file_tftp.__coderr = coderr

    def setMode(file_tftp, mode):
        file_tftp.__mode = mode

    def setDades(file_tftp, dades):
        file_tftp.__dades = dades

    def setError(file_tftp, error):
        file_tftp.__error = error

