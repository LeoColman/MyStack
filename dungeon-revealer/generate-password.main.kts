#!/usr/bin/env kotlin

import java.io.File
import java.util.*

val file = File("configuration.env")

val props = Properties().apply {
    load(file.inputStream())
}

val characters = ('a'..'z') + ('A'..'Z') + ('0'..'9') + ("!@#$%*()\\/".toList())
val dmPassword = List(10) { characters.random() }.joinToString("")
val pcPassword = List(10) { characters.random() }.joinToString("")
props["DM_PASSWORD"] = dmPassword
props["PC_PASSWORD"] = pcPassword

props.store(file.outputStream(), null)