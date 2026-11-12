package org.molecularis.app.ai
import org.junit.Assert.assertEquals
import org.junit.Test
class TaskRouterTest {
 @Test fun routesCodePrompt() { assertEquals(TaskKind.PROGRAMMING, TaskRouter().classify("debug my Kotlin code").task) }
 @Test fun defaultsToGeneral() { assertEquals(TaskKind.GENERAL, TaskRouter().classify("hello").task) }
}
