import json

class PlanEstudio():
    """
    Clase encargada de gestionar la carga del plan de estudio desde un archivo JSON.
    """

    def __init__(self, archivo="PlanEstudio2021.json"):
        """
        Inicializa la clase con el nombre del archivo del plan de estudio.

        Args:
            archivo (str): Ruta del archivo JSON que contiene el plan de estudio.
        """
        self.archivo = archivo

    def cargarPlanEstudio(self):
        """
        Carga el contenido del archivo JSON del plan de estudio.

        Returns:
            dict: Contenido completo del plan de estudio.
        """
        with open(self.archivo, "r", encoding="utf-8") as archivoPlan:
            self.plan2021 = json.load(archivoPlan)
        return self.plan2021


class UC():
    """
    Representa una unidad curricular (materia) del plan de estudio.
    """

    def __init__(self, plan: PlanEstudio, semestre: str, codigo: str):
        """
        Inicializa una unidad curricular (UC) a partir del plan de estudios, el semestre y el código asignado.

        Este constructor valida los argumentos recibidos y carga automáticamente los datos del plan
        para permitir el acceso posterior a la información de la materia.

        Args:
            plan (PlanEstudio): Objeto del plan de estudios previamente cargado.
            semestre (str): Clave que representa el semestre al que pertenece la UC (por ejemplo, "Semestre 1").
            codigo (str): Código identificador de la unidad curricular (por ejemplo, "S1UC1").

        Raises:
            ValueError: Si alguno de los argumentos no es del tipo esperado.
        """
        if isinstance(plan, PlanEstudio) and isinstance(semestre, str) and isinstance(codigo, str):
            self.plan = plan.cargarPlanEstudio()
            self.semestre = semestre
            self.codigo = codigo
        else:
            raise ValueError("Uno de los argumentos ingresados es incorrecto")

    def infoUC(self):
        """
        Carga y guarda la información asociada a la unidad curricular: nombre, previas y créditos.

        Este método busca la materia en el plan de estudios a partir del semestre y código proporcionados,
        y almacena sus datos internamente para poder ser utilizados por otros métodos.

        Returns:
            bool: True si los datos se cargaron correctamente.

        Raises:
            KeyError: Si los datos ingresados (semestre o código) no corresponden a ninguna materia válida.
        """
        try:
            info = self.plan[self.semestre][self.codigo]
            materia = info["Nombre"]
            previas = info["Previas"]
            creditos = info["Creditos"]
            self.infoMateria = (materia, previas, creditos)
            return True
        except:
            self.infoMateria = None
            raise KeyError ("La credenciales ingresadas son incorrectas")
        
    def nombreMateria(self):
        """
        Devuelve el nombre completo de la unidad curricular.

        Este método accede a la información cargada de la materia y retorna su nombre.
        Es necesario haber ejecutado previamente el método infoUC() para inicializar los datos.

        Returns:
            str: Nombre de la materia.

        Raises:
            TypeError: Si la información de la materia no ha sido cargada.
        """
        if self.infoMateria == None:
            raise TypeError("...")
        return self.infoMateria[0]

    def nombrePrevias(self):
        """
        Devuelve la lista de materias previas requeridas por la unidad curricular.

        Este método permite acceder a los nombres de las materias que deben estar
        aprobadas o cursadas antes de poder inscribirse en la actual. Requiere que
        la información haya sido cargada previamente con infoUC().

        Returns:
            list: Lista de materias previas de la unidad curricular.

        Raises:
            TypeError: Si la información de la materia no ha sido cargada.
        """
        if self.infoMateria == None:
            raise TypeError("Error: Códigos Incorrectos")
        return self.infoMateria[1]

    def getCreditos(self):
        """
        Devuelve la cantidad de créditos asignados a la unidad curricular.

        Este método extrae el valor de créditos desde la información de la materia.
        Si la información no fue cargada previamente mediante el método infoUC(), 
        lanza una excepción.

        Returns:
            int: Cantidad de créditos de la materia.

        Raises:
            TypeError: Si la información de la materia no ha sido inicializada.
        """
        if self.infoMateria == None:
            raise TypeError("...")
        return self.infoMateria[2]


class GestorExpediente:
    """
    Crea, carga y modifica archivos JSON para cada estudiante.
    Permite almacenar y gestionar sus datos.
    """

    def __init__(self, nombre: str, ci: int, añoIngreso: int):
        """
        Inicializa la clase con los datos del estudiante.

        Args:
            nombre (str): Nombre del estudiante.
            ci (int): Cédula de identidad del estudiante.
            añoIngreso (int): Año de ingreso a la carrera.
        """

        if not isinstance(nombre, str) or not nombre.strip():
            print("Error: El nombre del estudiante no puede estar vacío.")
            return False

        if not isinstance(ci, int) or ci <= 0:
            print("Error: La cédula debe ser un número entero positivo.")
            return False

        if not isinstance(añoIngreso, int) or añoIngreso < 2000 or añoIngreso > 2100:
            print("Error: El año de ingreso debe ser válido.")
            return False

        self.datos = {"Nombre": nombre,
                      "Cedula": ci,
                      "Año Ingreso": añoIngreso,
                      "Materias Aprobadas": [],
                      "Materias Matriculadas": [],
                      "Inscripción Examen": [],
                      "Créditos": 0}

        nombre_archivo = nombre.replace(" ", "_")
        self.archivo = f"{nombre_archivo}_{ci}.json"

    def crearArchivo(self, indentacion: int = 4):
        """
        Crea un archivo JSON para el estudiante con datos iniciales.

        Args:
            indentacion (int): Nivel de indentación para el formato JSON.
        """
        with open(self.archivo, 'w', encoding='utf-8') as file:
            json.dump(self.datos, file, ensure_ascii=False, indent=indentacion)

        self.data = self.datos
    
    def crear_registros(self, indentacion: int = 4):
        """
        Crea un archivo JSON para guardar las inscripciones de Matriculas y Examenes.

        Args:
            indentacion (int): Nivel de indentación para el formato JSON.
        """
        self.nombre_registros = "Registros.json"
        self.registros = {
            "Matriculas": {},
            "Examenes": {}}

        with open(self.nombre_registros, 'w', encoding='utf-8') as file:
            json.dump(self.registros, file, ensure_ascii=False, indent=indentacion)

    def cargarDatos(self, nombre_archivo:str):
        """
        Carga el contenido de un archivo JSON.
        Args:
            nombre_archivo: Nombre del archivo a cargar
        Returns:
            dict: Datos del estudiante.
        """
        with open(nombre_archivo, 'r', encoding='utf-8') as file:
            self.data = json.load(file)
        return self.data
    
    def actualizar_archivo(self, nombre_archivo, info):
        """
        Actualiza un archivo JSON
        Args:
            nombre_archivo: Nombre del archivo a modificar
            info: Nueva información para el archivo"""
        with open(nombre_archivo, 'w', encoding='utf-8') as file:
            json.dump(info, file, ensure_ascii=False, indent=4)

        self.data = info
        return True
    
    def _inscribir_examen(self, uc: UC):
        """
        Inscribe a un estudiante a examen
        Args:
            uc: Objeto UC"""
  
        datos = self.cargarDatos(self.archivo)
        nombre_uc = uc.nombreMateria()
        requisitos = uc.nombrePrevias()
        
        if nombre_uc in datos["Inscripción Examen"]:
            return False

        if not requisitos:
            datos["Inscripción Examen"].append(nombre_uc)
            self.actualizar_archivo(self.archivo, datos)
            self._registrar_inscripcion(uc, "Examen")
            return True
        else:
            for requisito in requisitos:
                if requisito not in datos["Materias Aprobadas"]:
                    return False
            datos["Inscripción Examen"].append(nombre_uc)
            self.actualizar_archivo(self.archivo, datos)
            self._registrar_inscripcion(uc, "Examen")
            return True
    
    def _quitar_examen(self, materia: UC):
        """
        Elimina una UC de la lista de inscripción a examen.

        Args:
            materia (UC): Objeto UC de la materia a eliminar"""
        datos = self.cargarDatos(self.archivo)
        uc = materia.nombreMateria()

        if uc in datos["Inscripción Examen"]:
            datos["Inscripción Examen"].remove(uc)
            self._eliminar_inscripcion(materia, "Examen")
        
        self.actualizar_archivo(self.archivo, datos)

    def _matricular_uc(self, uc: UC):
        """
        Matricula al estudiante en una Unidad Curricular (UC).

        Este método registra la matrícula del estudiante en una materia si cumple con los requisitos previos.
        Si la materia ya está aprobada o matriculada, no se vuelve a registrar. Al matricularse,
        se actualiza su expediente académico y se agrega su nombre al registro global de inscriptos.

        Args:
            uc (UC): Objeto que representa la unidad curricular a la que se desea matricular.

        Returns:
            bool: True si la matrícula fue registrada correctamente, False en caso contrario.
        """

        datos = self.cargarDatos(self.archivo)
        nombre_uc = uc.nombreMateria()
        requisitos = uc.nombrePrevias()
        
        if nombre_uc in datos["Materias Matriculadas"] or nombre_uc in datos["Materias Aprobadas"]:
            return False

        if not requisitos:
            datos["Materias Matriculadas"].append(nombre_uc)
            self.actualizar_archivo(self.archivo, datos)
            self._registrar_inscripcion(uc, "Matricula")
            return True
        else:
            for requisito in requisitos:
                if requisito not in datos["Materias Aprobadas"] and requisito not in datos["Materias Matriculadas"]:
                    return False
            datos["Inscripción Examen"].append(nombre_uc)
            self.actualizar_archivo(self.archivo, datos)
            self._registrar_inscripcion(uc, "Matricula")
            return True

    def _desmatricular_uc(self, materia: UC):
        """
        Desmatricula al estudiante de una Unidad Curricular (UC).

        Este método elimina la materia de la lista de materias matriculadas del estudiante,
        actualiza su expediente académico y remueve su nombre del registro global
        de inscriptos a esa unidad curricular en 'Registros.json'.

        Args:
            materia (UC): Objeto UC correspondiente a la materia que se desea desmatricular.
        """

        datos = self.cargarDatos(self.archivo)
        uc = materia.nombreMateria()

        if uc in datos["Materias Matriculadas"]:
            datos["Materias Matriculadas"].remove(uc)
            self._eliminar_inscripcion(materia, "Matricula")
        self.actualizar_archivo(self.archivo, datos)

    def _agregar_uc_aprobada(self, materia: UC):
        """
        Agrega una UC aprobada y suma sus créditos.
        Args:
            materia (UC): Objeto UC de la materia a agregar.
        Returns:
            bool: True si la materia se agregó correctamente.
        """
        datos = self.cargarDatos(self.archivo)
        uc = materia.nombreMateria()
        creditos = materia.getCreditos()

        if uc not in datos["Materias Aprobadas"]:
            datos["Materias Aprobadas"].append(uc)
            datos["Créditos"] += creditos

        self.actualizar_archivo(self.archivo, datos)
        return True
    
    def _quitar_uc_aprobada(self, materia: UC):
        """
        Elimina una UC aprobada y descuenta sus créditos.
        Args:
            materia (UC): Objeto UC de la materia a eliminar.
        """
        datos = self.cargarDatos(self.archivo)
        uc = materia.nombreMateria()
        creditos = materia.getCreditos()

        if uc in datos["Materias Aprobadas"]:
            datos["Materias Aprobadas"].remove(uc)
            datos["Créditos"] -= creditos

        self.actualizar_archivo(self.archivo, datos)
        return True

    def _registrar_inscripcion(self, materia: UC, instancia:str):
        """
        Registra al estudiante en el archivo 'Registros.json' como inscripto a una materia o examen.

        Este método se utiliza automáticamente cuando el estudiante se matricula o se inscribe a un examen.
        Agrega el nombre del estudiante a la lista correspondiente dentro del registro global,
        según la unidad curricular y el tipo de inscripción.

        Args:
            materia (UC): Objeto que representa la unidad curricular a la que se inscribe.
            instancia (str): Define el tipo de inscripción. Puede ser "Examen" o "Matricula".
        """
            
        uc = materia.nombreMateria()
        nombre = self.data['Nombre']

        self.contenido = self.cargarDatos(self.nombre_registros)

        if instancia == "Examen":    
            if uc not in self.contenido["Examenes"]:
                self.contenido["Examenes"][uc] = []
            if nombre not in self.contenido["Examenes"][uc]:
                self.contenido["Examenes"][uc].append(nombre)
        
        if instancia == "Matricula":
            if uc not in self.contenido["Matriculas"]:
                self.contenido["Matriculas"][uc] = []
            if nombre not in self.contenido["Matriculas"][uc]:
                self.contenido["Matriculas"][uc].append(nombre)
        
        self.actualizar_archivo(self.nombre_registros, self.contenido)
    
    def _eliminar_inscripcion(self, materia: UC, instancia:str):
        """
        Elimina al estudiante del registro global de inscripciones a una materia o examen.

        Este método actualiza el archivo 'Registros.json' para remover al estudiante 
        de la lista correspondiente, ya sea por desmatriculación o baja de examen.
        Se utiliza automáticamente al ejecutar los métodos _desmatricular_uc() o _quitar_examen().

        Args:
            materia (UC): Objeto UC correspondiente a la unidad curricular.
            instancia (str): Indica si se trata de una "Matricula" o un "Examen".
        """

        uc = materia.nombreMateria()
        nombre = self.data['Nombre']

        self.contenido = self.cargarDatos(self.nombre_registros)

        if instancia == "Examen":    
            if uc in self.contenido["Examenes"]:
                if nombre in self.contenido["Examenes"][uc]:
                    self.contenido["Examenes"][uc].remove(nombre)
        
        if instancia == "Matricula":
            if uc in self.contenido["Matriculas"]:
                if nombre in self.contenido["Matriculas"][uc]:
                    self.contenido["Matriculas"][uc].remove(nombre)
        
        self.actualizar_archivo(self.nombre_registros, self.contenido)

    def _inscriptos_examen(self):
        """
        Muestra los estudiantes inscriptos a exámenes.

        Este método accede al archivo global 'Registros.json' y devuelve un 
        diccionario donde cada clave representa una materia y su valor es 
        una lista con los nombres de los estudiantes inscriptos al examen 
        correspondiente.

        Se utiliza principalmente para consulta administrativa desde 
        la clase Secretaria.

        Returns:
            dict: Diccionario con materias como claves y listas de estudiantes como valores.
        """
        datos = self.cargarDatos(self.nombre_registros)
        inscriptos = datos["Examenes"]
        return inscriptos
    
    def _inscriptos_matriculas(self):
        """
        Muestra los estudiantes matriculados a diferentes Unidades Curriculares (UCs).

        Este método accede al archivo global 'Registros.json' y devuelve un 
        diccionario donde cada clave representa una unidad curricular (materia) 
        y su valor es una lista con los nombres de los estudiantes matriculados 
        en dicha materia.

        Se utiliza principalmente para consultas administrativas, por la clase Secretaria.

        Returns:
            dict: Diccionario con materias como claves y listas de estudiantes matriculados como valores.
        """
        datos = self.cargarDatos(self.nombre_registros)
        inscriptos = datos["Matriculas"]
        return inscriptos

class Estudiante():
    """
    Representa un estudiante y permite consultar sus datos académicos.
    """

    def __init__(self, usuario: GestorExpediente):
        """
        Inicializa el estudiante a partir de un archivo gestionado por GestorExpediente.

        Args:
            usuario (GestorExpediente): Gestor del archivo JSON del estudiante.
        """
        if isinstance (usuario, GestorExpediente):
            self.usuario = usuario

            self.estudiante = usuario.cargarDatos(self.usuario.archivo)
            self.nombre = self.estudiante["Nombre"]
            self.cedula = self.estudiante["Cedula"]
            self.aprobadas = self.estudiante["Materias Aprobadas"]
            self.matriculadas = self.estudiante["Materias Matriculadas"]
            self.examen = self.estudiante["Inscripción Examen"]
            self.creditos = self.estudiante["Créditos"]
        else:
            raise ValueError("Error: El expediente ingresado no es válido")
        
    def info_estudiante(self) -> tuple:
        """
        Devuelve nombre y cédula del estudiante.
        Returns:
            tuple: Nombre y cédula del estudiante.
        """
        return self.nombre, self.cedula

    def ucs_aprobadas(self) -> list:
        """
        Retorna una lista con las materias aprobadas del estudiante.
        Returns:
            list: Materias aprobadas.
        """
        return self.aprobadas

    def inscribir_examen(self, materia: UC):
        """
        Permite al estudiante inscribirse a un examen si cumple con las previas.
        Args:
            materia (UC): Objeto UC con la información de la materia.
        Returns:
            True si se realizo la inscripción
            False: si ocurrio un Error, el argumento proporcionado no es una unidad curricular válida.
        """
        try:
            self.usuario._inscribir_examen(materia)
            return True
        except:
            return False       

    def quitar_examen(self, materia: UC):
        """
        Elimina la inscripción del estudiante al examen de una Unidad Curricular (UC).

        Este método remueve la inscripción del estudiante al examen correspondiente,
        actualizando su expediente académico y el archivo global de registros.

        Args:
            materia (UC): Objeto que representa la unidad curricular del examen a eliminar.

        Returns:
            bool: True si la operación se realizó correctamente, False si ocurrió un error.
        """
        try:
            self.usuario._quitar_examen(materia)
            return True
        except:
            return False
    
    def matricular_uc(self, materia: UC):
        """
        Método para matricular al estudiante en una Unidad Curricular (UC).

        Este método permite que el estudiante quede registrado como cursante de una materia,
        siempre que cumpla con los requisitos previos definidos. Utiliza el gestor de expediente
        para realizar la validación y registrar la inscripción tanto en su archivo personal como 
        en el archivo 'Registros.json'.

        Args:
            materia (UC): Objeto que representa la materia a matricular.
        
        Returns:
            bool: True si la matrícula fue realizada correctamente, False si ocurrió un error.
        """
        try:
            self.usuario._matricular_uc(materia)
            return True
        except:
            return False 
    
    def desmatricular_uc(self, materia: UC):
        """
        Método para eliminar la matrícula del estudiante en una Unidad Curricular (UC).

        Este método remueve la materia de la lista de cursadas del estudiante,
        actualizando su expediente académico y el archivo 'Registros.json'.
        Es útil cuando el estudiante decide abandonar una materia antes de finalizarla.

        Args:
            materia (UC): Objeto que representa la materia a desmatricular.
        
        Returns:
            bool: True si se ejecuta correctamente (aunque no valida si estaba inscripto).
        """
        self.usuario._desmatricular_uc(materia)
        return True

    def __str__(self):
        """
        Representación en string del estudiante.
        Returns:
            str: Información básica del estudiante.
        """
        return (f"Información del estudiante:\n"
                f"Nombre: {self.nombre}\n"
                f"C.I: {self.cedula}\n"
                f"Materias aprobadas: {self.aprobadas}\n"
                f"Materias Matriculadas: {self.matriculadas}\n"
                f"Inscripcion Examenes: {self.examen}\n"
                f"Créditos: {self.creditos}")
class Secretaria():
    """ 
    Representa a la coordinadora y secretaria académica.
    """

    def __init__(self, nombre: str):
        """
        Inicializa un objeto de la clase Secretaria con su nombre.

        Valida que el nombre proporcionado sea una cadena de texto.
        Si no lo es, lanza un error.

        Args:
            nombre (str): Nombre de la secretaria.

        Raises:
            NameError: Si el valor ingresado no es un string.
        """
        if not isinstance(nombre, str):
            raise NameError ("Error: Ingrese un nombre")
        
        self.nombre = nombre

    def cargar_estudiante(self, expediente: GestorExpediente):
        """
        Asocia un expediente académico al objeto Secretaria.

        Este método permite cargar el expediente de un estudiante
        para que la secretaria pueda realizar operaciones administrativas
        sobre sus datos académicos.

        Args:
            expediente (GestorExpediente): Objeto que representa el expediente del estudiante.

        Returns:
            bool: True si el expediente es válido y fue cargado correctamente, False en caso contrario.
        """
        if isinstance(expediente, GestorExpediente):
            self.expediente = expediente
            return True
        else:
            return False

    def inscribir_examen(self, materia: UC):
        """
        Inscribe al estudiante a un examen.
        Args:
            materia (UC): Objeto UC al que se quiere inscribir.
        Returns:
                True: Se inscribio al examen correctamente
                Faslse: Hubo un error al inscribir al estudiante a examen
        """
        try:
            self.expediente._inscribir_examen(materia)
            return True
        except:
            return False 

    def quitar_examen(self, materia: UC):
        """
        Elimina la inscripción del estudiante al examen de la unidad curricular indicada.

        Este método actualiza el expediente académico y los registros globales,
        removiendo la inscripción al examen si la materia estaba registrada.

        Args:
            materia (UC): Objeto UC correspondiente a la materia de la que se desea quitar el examen.

        Returns:
            bool: True si se eliminó correctamente, False si ocurrió un error.
        """
        try:
            self.expediente._quitar_examen(materia)
            return True
        except:
            return False
    
    def matricular_uc(self, materia: UC):
        """
        Matricula al estudiante en una Unidad Curricular (UC).

        Intenta registrar al estudiante como cursante de la materia indicada,
        validando automáticamente si cumple con los requisitos previos definidos
        en el plan de estudios. Si no cumple las condiciones, no se registra.

        Args:
            materia (UC): Objeto UC que representa la materia a matricular.

        Returns:
            bool: True si la matrícula se realizó correctamente, False en caso contrario.
        """
        try:
            self.expediente._matricular_uc(materia)
            return True
        except:
            return False

    def desmatricular_uc(self, materia: UC):
        """
        Elimina la matrícula del estudiante en una Unidad Curricular (UC).

        Este método remueve una materia del listado de cursadas del estudiante,
        actualizando tanto su archivo individual como el archivo de registros.json.

        Args:
            materia (UC): Objeto UC que representa la materia a desmatricular.
        """
        self.expediente._desmatricular_uc(materia)
    
    def agregar_uc_aprobada(self, aprobada: UC) -> bool:
        """
        Agrega una materia aprobada al expediente del estudiante.
        Args:
            aprobada (UC): Objeto UC de la materia a agregar.
        Returns:
            bool: True si se agregó correctamente, False si hubo un error.
        """
        self.expediente._agregar_uc_aprobada(aprobada)
        return True
    
    def quitar_uc_aprobada(self, materia: UC) -> bool:
        """
        Elimina una UC aprobada del expediente.
        Args:
            materia (UC): Objeto UC de la materia a eliminar.
        Returns:
            bool: True si se eliminó correctamente.
        """
        self.expediente._quitar_uc_aprobada(materia)
        return True
    
    def ver_inscriptos_examen(self):
        """
        Devuelve la lista de estudiantes inscriptos a exámenes.

        Este método permite consultar el archivo de registros
        para obtener qué estudiantes se han anotado a rendir examen
        en cada Unidad Curricular (UC).

        Returns:
            dict: Diccionario con materias como claves y listas de estudiantes inscriptos como valores.
        """
        return self.expediente._inscriptos_examen()
    
    def ver_inscriptos_matriculas(self):
        """
        Devuelve la lista de estudiantes matriculados en Unidades Curriculares (UCs).

        Este método accede al archivo de registros para consultar
        qué estudiantes están actualmente cursando cada materia del plan.

        Returns:
            dict: Diccionario con materias como claves y listas de estudiantes matriculados como valores.
        """
        return self.expediente._inscriptos_matriculas()