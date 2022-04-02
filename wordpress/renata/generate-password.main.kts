#!/usr/bin/env kotlin

import java.io.File
import java.util.*

val file = File("config.env")

val props = Properties().apply {
    load(file.inputStream())
}

val characters = ('a'..'z') + ('A'..'Z') + ('0'..'9') + ("!@#$%*()\\/".toList())
val password = List(10) { characters.random() }.joinToString("")
props["MYSQL_PASSWORD"] = password
props["MYSQL_ROOT_PASSWORD"] = password
props["WORDPRESS_DB_PASSWORD"] = password

props.store(file.outputStream(), null)