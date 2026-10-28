package com.example.task.presentation

import app.cash.turbine.test
import com.example.task.domain.Task
import com.example.task.domain.TaskRepository
import io.mockk.coEvery
import io.mockk.coVerify
import io.mockk.mockk
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.test.*
import org.junit.After
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Before
import org.junit.Test

@OptIn(ExperimentalCoroutinesApi::class)
class TaskViewModelTest {

    private val repository: TaskRepository = mockk(relaxed = true)
    private val testDispatcher = StandardTestDispatcher()
    private lateinit var viewModel: TaskViewModel

    @Before
    fun setUp() {
        Dispatchers.setMain(testDispatcher)
    }

    @After
    fun tearDown() {
        Dispatchers.resetMain()
    }

    @Test
    fun `loadTasks success emits Loading then Success state`() = runTest(testDispatcher) {
        val mockTasks = listOf(
            Task(id = "1", title = "Compose UI Test", isCompleted = false),
            Task(id = "2", title = "ViewModel Unit Test", isCompleted = true)
        )
        coEvery { repository.getTasks() } returns flowOf(mockTasks)

        viewModel = TaskViewModel(repository)

        viewModel.uiState.test {
            // Initial loading state
            assertEquals(TaskUiState.Loading, awaitItem())

            // Advance coroutines
            testScheduler.advanceUntilIdle()

            // Success state
            val success = awaitItem() as TaskUiState.Success
            assertEquals(2, success.tasks.size)
            assertEquals("Compose UI Test", success.tasks[0].title)

            cancelAndIgnoreRemainingEvents()
        }
    }

    @Test
    fun `toggleTask calls repository toggle method`() = runTest(testDispatcher) {
        coEvery { repository.getTasks() } returns flowOf(emptyList())
        viewModel = TaskViewModel(repository)
        testScheduler.advanceUntilIdle()

        viewModel.toggleTask("task_123")
        testScheduler.advanceUntilIdle()

        coVerify(exactly = 1) { repository.toggleTaskCompletion("task_123") }
    }
}
