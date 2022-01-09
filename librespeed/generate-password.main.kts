import java.io.File
import java.util.*

val file = File("config.env")

val props = Properties().apply {
    load(file.inputStream())
}

val characters = ('a'..'z') + ('A'..'Z') + ('0'..'9') + ("!@#$%*()\\/".toList())
val password = List(10) { characters.random() }.joinToString("")
props["PASSWORD"] = password

props.store(file.outputStream(), null)