import java.io.File
import java.util.Properties

val characters = ('a'..'z') + ('A'..'Z') + ('0'..'9')
val password = List(10) { characters.random() }.joinToString("")


val props = Properties()
props["ServerIP"] = "192.168.1.2"
props["TZ"] = "America/Sao_Paulo"
props["WEBPASSWORD"] = password

props.store(File("config.env").outputStream(), null)
