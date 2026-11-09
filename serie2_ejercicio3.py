"""Serie II, ejercicio 3: aplicación de biblioteca (libros, socios y préstamos).

Serie II, ejercicio 1. Una biblioteca registra libros (ISBN, título, autor,
disponible) y socios (carné, nombre). Un socio puede tener de 0 a 3 préstamos
activos; cada préstamo es de un solo libro y guarda la fecha de salida y la
fecha de devolución.

Para ejecutarlo en IDLE: abrir este archivo y presionar F5. Al iniciar se elige:
1) demostración automática del resultado, 2) la aplicación con menú, 3) pruebas.
"""
import unittest
from datetime import date


class BibliotecaError(Exception):
    """Excepción base de los errores de la biblioteca."""


class DatoInvalidoError(BibliotecaError):
    """Un dato está vacío o no es válido."""


class RegistroDuplicadoError(BibliotecaError):
    """Ya existe un libro o un socio con ese identificador."""


class RegistroNoEncontradoError(BibliotecaError):
    """No existe un libro o un socio con ese identificador."""


class LibroNoDisponibleError(BibliotecaError):
    """El libro ya está prestado."""


class LimitePrestamosError(BibliotecaError):
    """El socio ya tiene el máximo de préstamos activos."""


class PrestamoNoEncontradoError(BibliotecaError):
    """El socio no tiene prestado ese libro."""


def limpiar_texto(valor, campo):
    """Quita espacios extra y verifica que el texto no quede vacío.

    Args:
        valor: texto escrito por el usuario.
        campo: nombre del dato (para el mensaje de error).

    Returns:
        El texto sin espacios de más.

    Raises:
        DatoInvalidoError: si el texto queda vacío.
    """
    texto = " ".join(str(valor).split())
    if not texto:
        raise DatoInvalidoError(f"{campo} no puede estar vacío.")
    return texto


class Libro:
    """Libro de la biblioteca: ISBN, título, autor y si está disponible."""

    def __init__(self, isbn, titulo, autor, disponible=True):
        """Crea un libro.

        Args:
            isbn: identificador único del libro.
            titulo: título del libro.
            autor: autor del libro.
            disponible: True si se puede prestar.

        Raises:
            DatoInvalidoError: si algún dato está vacío.
        """
        self._isbn = self.normalizar_isbn(isbn)
        self._titulo = limpiar_texto(titulo, "El título")
        self._autor = limpiar_texto(autor, "El autor")
        self._disponible = bool(disponible)

    @staticmethod
    def normalizar_isbn(isbn):
        """Devuelve el ISBN sin espacios y en mayúsculas."""
        return limpiar_texto(isbn, "El ISBN").replace(" ", "").upper()

    @property
    def isbn(self):
        """ISBN del libro."""
        return self._isbn

    @property
    def titulo(self):
        """Título del libro."""
        return self._titulo

    @property
    def autor(self):
        """Autor del libro."""
        return self._autor

    def esta_disponible(self):
        """Indica si el libro se puede prestar.

        Returns:
            True si está disponible, False si está prestado.
        """
        return self._disponible

    def prestar(self):
        """Marca el libro como prestado.

        Raises:
            LibroNoDisponibleError: si el libro ya estaba prestado.
        """
        if not self._disponible:
            raise LibroNoDisponibleError(
                f"El libro '{self._titulo}' no está disponible: ya está prestado.")
        self._disponible = False

    def devolver(self):
        """Marca el libro como disponible otra vez."""
        self._disponible = True

    def __str__(self):
        """Texto legible del libro."""
        estado = "Disponible" if self._disponible else "Prestado"
        return f"{self._isbn} | {self._titulo} | {self._autor} | {estado}"


class Prestamo:
    """Préstamo de un solo libro a un socio, con fecha de salida y devolución.

    Mientras el libro no se devuelve, la fecha de devolución es None y el
    préstamo está activo.
    """

    def __init__(self, socio, libro, fecha_salida=None):
        """Crea un préstamo.

        Args:
            socio: socio que recibe el libro.
            libro: libro prestado.
            fecha_salida: fecha de salida (por defecto, hoy).
        """
        self._socio = socio
        self._libro = libro
        self._fecha_salida = fecha_salida or date.today()
        self._fecha_devolucion = None

    @property
    def socio(self):
        """Socio que tiene el libro."""
        return self._socio

    @property
    def libro(self):
        """Libro prestado."""
        return self._libro

    @property
    def fecha_salida(self):
        """Fecha en que salió el libro."""
        return self._fecha_salida

    @property
    def fecha_devolucion(self):
        """Fecha en que se devolvió el libro (None si sigue prestado)."""
        return self._fecha_devolucion

    def esta_activo(self):
        """Indica si el libro todavía no se ha devuelto.

        Returns:
            True si el préstamo sigue activo.
        """
        return self._fecha_devolucion is None

    def registrar_devolucion(self, fecha=None):
        """Guarda la fecha de devolución y cierra el préstamo.

        Args:
            fecha: fecha de devolución (por defecto, hoy).

        Raises:
            DatoInvalidoError: si el préstamo ya estaba cerrado o si la fecha
                es anterior a la de salida.
        """
        if not self.esta_activo():
            raise DatoInvalidoError("Este préstamo ya fue devuelto.")
        fecha = fecha or date.today()
        if fecha < self._fecha_salida:
            raise DatoInvalidoError(
                "La fecha de devolución no puede ser anterior a la de salida.")
        self._fecha_devolucion = fecha

    def __str__(self):
        """Texto legible del préstamo."""
        devolucion = self._fecha_devolucion or "(activo)"
        return (f"{self._socio.carne} | {self._libro.titulo} | "
                f"salida {self._fecha_salida} | devolución {devolucion}")


class Socio:
    """Socio de la biblioteca. Puede tener de 0 a 3 préstamos activos."""

    MAX_PRESTAMOS = 3

    def __init__(self, carne, nombre):
        """Crea un socio.

        Args:
            carne: identificador único del socio.
            nombre: nombre del socio.

        Raises:
            DatoInvalidoError: si algún dato está vacío.
        """
        self._carne = self.normalizar_carne(carne)
        self._nombre = limpiar_texto(nombre, "El nombre")
        self._prestamos = []

    @staticmethod
    def normalizar_carne(carne):
        """Devuelve el carné sin espacios y en mayúsculas."""
        return limpiar_texto(carne, "El carné").replace(" ", "").upper()

    @property
    def carne(self):
        """Carné del socio."""
        return self._carne

    @property
    def nombre(self):
        """Nombre del socio."""
        return self._nombre

    @property
    def prestamos(self):
        """Historial completo de préstamos (activos y devueltos)."""
        return list(self._prestamos)

    def prestamos_activos(self):
        """Devuelve los préstamos que todavía no se han devuelto.

        Returns:
            Lista con 0 a 3 préstamos.
        """
        return [p for p in self._prestamos if p.esta_activo()]

    def prestar(self, libro, fecha_salida=None):
        """Presta un libro a este socio.

        Args:
            libro: libro que se presta.
            fecha_salida: fecha de salida (por defecto, hoy).

        Returns:
            El Prestamo creado.

        Raises:
            LimitePrestamosError: si ya tiene 3 préstamos activos.
            LibroNoDisponibleError: si el libro ya está prestado.
        """
        if len(self.prestamos_activos()) >= self.MAX_PRESTAMOS:
            raise LimitePrestamosError(
                f"{self._nombre} ya tiene {self.MAX_PRESTAMOS} préstamos activos "
                f"(el máximo permitido).")
        prestamo = Prestamo(self, libro, fecha_salida)
        libro.prestar()
        self._prestamos.append(prestamo)
        return prestamo

    def devolver(self, libro, fecha_devolucion=None):
        """Devuelve un libro que este socio tiene prestado.

        Args:
            libro: libro que se devuelve.
            fecha_devolucion: fecha de devolución (por defecto, hoy).

        Returns:
            El Prestamo cerrado.

        Raises:
            PrestamoNoEncontradoError: si el socio no tiene ese libro.
            DatoInvalidoError: si la fecha es anterior a la de salida.
        """
        for prestamo in self.prestamos_activos():
            if prestamo.libro is libro:
                prestamo.registrar_devolucion(fecha_devolucion)
                libro.devolver()
                return prestamo
        raise PrestamoNoEncontradoError(
            f"{self._nombre} no tiene prestado el libro '{libro.titulo}'.")

    def __str__(self):
        """Texto legible del socio."""
        return (f"{self._carne} | {self._nombre} | préstamos activos: "
                f"{len(self.prestamos_activos())}/{self.MAX_PRESTAMOS}")


class Biblioteca:
    """Biblioteca: registra libros y socios y coordina los préstamos."""

    def __init__(self, nombre="Biblioteca Central"):
        """Crea una biblioteca vacía.

        Args:
            nombre: nombre de la biblioteca.
        """
        self._nombre = nombre
        self._libros = {}
        self._socios = {}

    @property
    def nombre(self):
        """Nombre de la biblioteca."""
        return self._nombre

    def registrar_libro(self, isbn, titulo, autor):
        """Registra un libro nuevo (queda disponible).

        Returns:
            El Libro creado.

        Raises:
            RegistroDuplicadoError: si el ISBN ya existe.
            DatoInvalidoError: si algún dato está vacío.
        """
        libro = Libro(isbn, titulo, autor)
        if libro.isbn in self._libros:
            raise RegistroDuplicadoError(f"Ya existe un libro con el ISBN {libro.isbn}.")
        self._libros[libro.isbn] = libro
        return libro

    def registrar_socio(self, carne, nombre):
        """Registra un socio nuevo.

        Returns:
            El Socio creado.

        Raises:
            RegistroDuplicadoError: si el carné ya existe.
            DatoInvalidoError: si algún dato está vacío.
        """
        socio = Socio(carne, nombre)
        if socio.carne in self._socios:
            raise RegistroDuplicadoError(f"Ya existe un socio con el carné {socio.carne}.")
        self._socios[socio.carne] = socio
        return socio

    def buscar_libro(self, isbn):
        """Busca un libro por ISBN.

        Raises:
            RegistroNoEncontradoError: si no existe.
        """
        clave = Libro.normalizar_isbn(isbn)
        if clave not in self._libros:
            raise RegistroNoEncontradoError(f"No existe un libro con el ISBN {clave}.")
        return self._libros[clave]

    def buscar_socio(self, carne):
        """Busca un socio por carné.

        Raises:
            RegistroNoEncontradoError: si no existe.
        """
        clave = Socio.normalizar_carne(carne)
        if clave not in self._socios:
            raise RegistroNoEncontradoError(f"No existe un socio con el carné {clave}.")
        return self._socios[clave]

    def libros(self):
        """Devuelve todos los libros, ordenados por título."""
        return sorted(self._libros.values(), key=lambda libro: libro.titulo)

    def socios(self):
        """Devuelve todos los socios, ordenados por nombre."""
        return sorted(self._socios.values(), key=lambda socio: socio.nombre)

    def prestar(self, carne, isbn, fecha_salida=None):
        """Presta el libro con ese ISBN al socio con ese carné.

        Returns:
            El Prestamo creado.

        Raises:
            RegistroNoEncontradoError, LimitePrestamosError,
            LibroNoDisponibleError.
        """
        socio = self.buscar_socio(carne)
        libro = self.buscar_libro(isbn)
        return socio.prestar(libro, fecha_salida)

    def devolver(self, carne, isbn, fecha_devolucion=None):
        """Registra la devolución de un libro.

        Returns:
            El Prestamo cerrado.

        Raises:
            RegistroNoEncontradoError, PrestamoNoEncontradoError,
            DatoInvalidoError.
        """
        socio = self.buscar_socio(carne)
        libro = self.buscar_libro(isbn)
        return socio.devolver(libro, fecha_devolucion)

    def historial_prestamos(self):
        """Devuelve todos los préstamos (activos y devueltos) por fecha de salida."""
        todos = [p for socio in self._socios.values() for p in socio.prestamos]
        return sorted(todos, key=lambda prestamo: prestamo.fecha_salida)

    def cargar_datos_de_ejemplo(self):
        """Registra 6 libros y 3 socios de ejemplo para probar la aplicación."""
        for isbn, titulo, autor in [
            ("ISBN-001", "Cien años de soledad", "Gabriel García Márquez"),
            ("ISBN-002", "Don Quijote de la Mancha", "Miguel de Cervantes"),
            ("ISBN-003", "El Principito", "Antoine de Saint-Exupéry"),
            ("ISBN-004", "Rayuela", "Julio Cortázar"),
            ("ISBN-005", "Pedro Páramo", "Juan Rulfo"),
            ("ISBN-006", "Introducción a Python", "Autor de Ejemplo"),
        ]:
            self.registrar_libro(isbn, titulo, autor)
        for carne, nombre in [("C001", "Ana Pérez"), ("C002", "Luis Gómez"),
                              ("C003", "María López")]:
            self.registrar_socio(carne, nombre)


class AppBiblioteca:
    """Interfaz de consola de la biblioteca."""

    def __init__(self, biblioteca=None):
        """Crea la aplicación.

        Args:
            biblioteca: biblioteca a usar; si es None se crea una con datos
                de ejemplo.
        """
        if biblioteca is None:
            biblioteca = Biblioteca()
            biblioteca.cargar_datos_de_ejemplo()
        self._biblioteca = biblioteca
        self._activa = True
        self._acciones = {
            "1": self._registrar_libro,
            "2": self._registrar_socio,
            "3": self._prestar,
            "4": self._devolver,
            "5": self.ver_libros,
            "6": self.ver_socios,
            "7": self.ver_historial,
            "8": self._salir,
        }

    def ejecutar(self):
        """Muestra el menú y ejecuta la opción elegida hasta que se salga."""
        while self._activa:
            print(f"\n=== {self._biblioteca.nombre.upper()} ===")
            print("1) Registrar libro\n2) Registrar socio\n3) Prestar libro\n"
                  "4) Devolver libro\n5) Ver libros\n6) Ver socios y sus préstamos\n"
                  "7) Ver historial de préstamos\n8) Salir")
            accion = self._acciones.get(input("Elija una opción: ").strip())
            if accion is None:
                print("Error: opción no válida.")
                continue
            try:
                accion()
            except BibliotecaError as error:
                print(f"Error: {error}")

    def _registrar_libro(self):
        """Opción 1: registra un libro nuevo."""
        libro = self._biblioteca.registrar_libro(
            input("ISBN: "), input("Título: "), input("Autor: "))
        print(f"Libro registrado: {libro}")

    def _registrar_socio(self):
        """Opción 2: registra un socio nuevo."""
        socio = self._biblioteca.registrar_socio(input("Carné: "), input("Nombre: "))
        print(f"Socio registrado: {socio}")

    def _prestar(self):
        """Opción 3: presta un libro a un socio."""
        prestamo = self._biblioteca.prestar(input("Carné del socio: "), input("ISBN del libro: "))
        print(f"Préstamo registrado: {prestamo}")

    def _devolver(self):
        """Opción 4: registra la devolución de un libro."""
        prestamo = self._biblioteca.devolver(input("Carné del socio: "), input("ISBN del libro: "))
        print(f"Devolución registrada: {prestamo}")

    def ver_libros(self):
        """Opción 5: muestra todos los libros y si están disponibles."""
        print(f"{'ISBN':<10}{'Título':<30}{'Autor':<28}{'Estado':<12}")
        print("-" * 80)
        for libro in self._biblioteca.libros():
            estado = "Disponible" if libro.esta_disponible() else "Prestado"
            print(f"{libro.isbn:<10}{libro.titulo:<30}{libro.autor:<28}{estado:<12}")

    def ver_socios(self):
        """Opción 6: muestra los socios con sus préstamos activos."""
        for socio in self._biblioteca.socios():
            print(socio)
            for prestamo in socio.prestamos_activos():
                print(f"    - {prestamo.libro.titulo} (salida {prestamo.fecha_salida})")

    def ver_historial(self):
        """Opción 7: muestra todos los préstamos con sus fechas."""
        print(f"{'Carné':<8}{'Libro':<30}{'Salida':<12}{'Devolución':<12}")
        print("-" * 62)
        for p in self._biblioteca.historial_prestamos():
            devolucion = str(p.fecha_devolucion) if p.fecha_devolucion else "(activo)"
            print(f"{p.socio.carne:<8}{p.libro.titulo:<30}{str(p.fecha_salida):<12}{devolucion:<12}")
        if not self._biblioteca.historial_prestamos():
            print("Todavía no hay préstamos.")

    def _salir(self):
        """Opción 8: termina la aplicación."""
        print("¡Hasta pronto!")
        self._activa = False



class Demostracion:
    """Ejecuta un caso completo de la biblioteca y muestra el resultado."""

    def __init__(self):
        """Crea una biblioteca con datos de ejemplo para la demostración."""
        self._biblioteca = Biblioteca()
        self._biblioteca.cargar_datos_de_ejemplo()
        self._app = AppBiblioteca(self._biblioteca)

    def _paso(self, titulo, accion, *argumentos):
        """Ejecuta una acción, muestra su resultado y los errores controlados.

        Args:
            titulo: descripción del paso.
            accion: método de la biblioteca que se ejecuta.
            argumentos: datos que recibe la acción.
        """
        print(f"\n>> {titulo}")
        try:
            print(f"   Resultado: {accion(*argumentos)}")
        except BibliotecaError as error:
            print(f"   Error controlado: {error}")

    def ejecutar(self):
        """Muestra el caso completo: préstamos, límite de 3, devoluciones e historial."""
        b = self._biblioteca
        salida = date(2026, 11, 2)
        print("=== SERIE II, EJERCICIO 3: RESULTADO DE LA APLICACIÓN ===")
        print("\nLibros al inicio:")
        self._app.ver_libros()
        self._paso("Prestar ISBN-001 a C001 (Ana Pérez)", b.prestar, "C001", "ISBN-001", salida)
        self._paso("Prestar ISBN-002 a C001", b.prestar, "C001", "ISBN-002", salida)
        self._paso("Prestar ISBN-003 a C001", b.prestar, "C001", "ISBN-003", salida)
        self._paso("Prestar un 4.º libro (ISBN-004) a C001: debe fallar, el máximo es 3",
                   b.prestar, "C001", "ISBN-004", salida)
        self._paso("Prestar ISBN-001 a C002: debe fallar, el libro ya está prestado",
                   b.prestar, "C002", "ISBN-001", salida)
        print("\nSocios y sus préstamos activos:")
        self._app.ver_socios()
        self._paso("Devolver ISBN-001 (C001) el 2026-11-09", b.devolver, "C001", "ISBN-001", date(2026, 11, 9))
        self._paso("Devolver ISBN-005 (C001): debe fallar, no lo tiene prestado",
                   b.devolver, "C001", "ISBN-005", date(2026, 11, 9))
        self._paso("Prestar ISBN-001 a C002: ahora sí está disponible", b.prestar, "C002", "ISBN-001", date(2026, 11, 10))
        print("\nHistorial de préstamos (fecha de salida y de devolución):")
        self._app.ver_historial()
        print("\nLibros al final:")
        self._app.ver_libros()


class PruebasBiblioteca(unittest.TestCase):
    """Comprueba las reglas de la biblioteca."""

    def setUp(self):
        """Crea una biblioteca con los datos de ejemplo antes de cada prueba."""
        self.bib = Biblioteca()
        self.bib.cargar_datos_de_ejemplo()

    def test_libro_nuevo_esta_disponible(self):
        self.assertTrue(self.bib.buscar_libro("ISBN-001").esta_disponible())

    def test_socio_nuevo_tiene_cero_prestamos(self):
        self.assertEqual(len(self.bib.buscar_socio("C001").prestamos_activos()), 0)

    def test_prestar_deja_el_libro_no_disponible(self):
        self.bib.prestar("C001", "ISBN-001")
        self.assertFalse(self.bib.buscar_libro("ISBN-001").esta_disponible())
        self.assertEqual(len(self.bib.buscar_socio("C001").prestamos_activos()), 1)

    def test_no_se_puede_prestar_un_libro_ya_prestado(self):
        self.bib.prestar("C001", "ISBN-001")
        with self.assertRaises(LibroNoDisponibleError):
            self.bib.prestar("C002", "ISBN-001")
        self.assertEqual(len(self.bib.buscar_socio("C002").prestamos_activos()), 0)

    def test_maximo_tres_prestamos_activos(self):
        for isbn in ("ISBN-001", "ISBN-002", "ISBN-003"):
            self.bib.prestar("C001", isbn)
        with self.assertRaises(LimitePrestamosError):
            self.bib.prestar("C001", "ISBN-004")
        self.assertTrue(self.bib.buscar_libro("ISBN-004").esta_disponible())
        self.assertEqual(len(self.bib.buscar_socio("C001").prestamos_activos()), 3)

    def test_devolver_libera_el_libro_y_el_cupo(self):
        for isbn in ("ISBN-001", "ISBN-002", "ISBN-003"):
            self.bib.prestar("C001", isbn)
        self.bib.devolver("C001", "ISBN-001")
        self.assertTrue(self.bib.buscar_libro("ISBN-001").esta_disponible())
        self.bib.prestar("C001", "ISBN-004")
        self.assertEqual(len(self.bib.buscar_socio("C001").prestamos_activos()), 3)

    def test_devolver_un_libro_que_no_tiene_prestado(self):
        with self.assertRaises(PrestamoNoEncontradoError):
            self.bib.devolver("C001", "ISBN-005")

    def test_el_prestamo_guarda_fecha_de_salida_y_de_devolucion(self):
        prestamo = self.bib.prestar("C001", "ISBN-001", date(2026, 11, 1))
        self.assertEqual(prestamo.fecha_salida, date(2026, 11, 1))
        self.assertIsNone(prestamo.fecha_devolucion)
        self.assertTrue(prestamo.esta_activo())
        self.bib.devolver("C001", "ISBN-001", date(2026, 11, 8))
        self.assertEqual(prestamo.fecha_devolucion, date(2026, 11, 8))
        self.assertFalse(prestamo.esta_activo())

    def test_la_devolucion_no_puede_ser_anterior_a_la_salida(self):
        self.bib.prestar("C001", "ISBN-001", date(2026, 11, 10))
        with self.assertRaises(DatoInvalidoError):
            self.bib.devolver("C001", "ISBN-001", date(2026, 11, 1))

    def test_el_historial_conserva_los_prestamos_devueltos(self):
        self.bib.prestar("C001", "ISBN-001")
        self.bib.devolver("C001", "ISBN-001")
        self.assertEqual(len(self.bib.historial_prestamos()), 1)
        self.assertEqual(len(self.bib.buscar_socio("C001").prestamos_activos()), 0)

    def test_no_se_permiten_registros_duplicados(self):
        with self.assertRaises(RegistroDuplicadoError):
            self.bib.registrar_libro("isbn-001", "Otro", "Otro autor")
        with self.assertRaises(RegistroDuplicadoError):
            self.bib.registrar_socio("c001", "Otra persona")

    def test_buscar_algo_que_no_existe(self):
        with self.assertRaises(RegistroNoEncontradoError):
            self.bib.buscar_libro("XXX")
        with self.assertRaises(RegistroNoEncontradoError):
            self.bib.buscar_socio("XXX")

    def test_datos_vacios_no_se_aceptan(self):
        with self.assertRaises(DatoInvalidoError):
            self.bib.registrar_libro("ISBN-100", "   ", "Autor")


def ejecutar_pruebas():
    """Ejecuta las pruebas automáticas y muestra el resultado."""
    cargador = unittest.defaultTestLoader.loadTestsFromTestCase(PruebasBiblioteca)
    unittest.TextTestRunner(verbosity=2).run(cargador)


if __name__ == "__main__":
    print("1) Ver la demostración automática (resultado del ejercicio)")
    print("2) Usar la aplicación con menú")
    print("3) Ejecutar las pruebas automáticas")
    eleccion = input("Elija una opción: ").strip()
    if eleccion == "1":
        Demostracion().ejecutar()
    elif eleccion == "3":
        ejecutar_pruebas()
    else:
        AppBiblioteca().ejecutar()
