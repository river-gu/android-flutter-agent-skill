package com.example.task.presentation

import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createComposeRule
import com.example.task.domain.Task
import com.example.task.domain.TaskRepository
import io.mockk.every
import io.mockk.mockk
import kotlinx.coroutines.flow.MutableStateFlow
import org.junit.Rule
import org.junit.Test

class TaskListScreenTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    private val repository: TaskRepository = mockk(relaxed = true)

    @Test
    fun taskListScreen_displaysLoadingIndicator_whenStateIsLoading() {
        val fakeStateFlow = MutableStateFlow<TaskUiState>(TaskUiState.Loading)
        val mockViewModel = mockk<TaskViewModel>(relaxed = true) {
            every { uiState } returns fakeStateFlow
        }

        composeTestRule.setContent {
            TaskListScreen(
                viewModel = mockViewModel,
                onNavigateToDetail = {}
            )
        }

        // Verify loading indicator is present
        composeTestRule.onNode(hasProgressBarRangeInfo(ProgressBarRangeInfo.Indeterminate))
            .assertIsDisplayed()
    }

    @Test
    fun taskListScreen_displaysEmptyMessage_whenStateIsEmpty() {
        val fakeStateFlow = MutableStateFlow<TaskUiState>(TaskUiState.Empty)
        val mockViewModel = mockk<TaskViewModel>(relaxed = true) {
            every { uiState } returns fakeStateFlow
        }

        composeTestRule.setContent {
            TaskListScreen(
                viewModel = mockViewModel,
                onNavigateToDetail = {}
            )
        }

        composeTestRule.onNodeWithText("No tasks available. Tap to create one!")
            .assertIsDisplayed()
    }

    @Test
    fun taskListScreen_displaysTasks_whenStateIsSuccess() {
        val tasks = listOf(
            Task(id = "1", title = "Write Unit Tests", isCompleted = false)
        )
        val fakeStateFlow = MutableStateFlow<TaskUiState>(TaskUiState.Success(tasks))
        val mockViewModel = mockk<TaskViewModel>(relaxed = true) {
            every { uiState } returns fakeStateFlow
        }

        composeTestRule.setContent {
            TaskListScreen(
                viewModel = mockViewModel,
                onNavigateToDetail = {}
            )
        }

        composeTestRule.onNodeWithText("Write Unit Tests").assertIsDisplayed()
        composeTestRule.onNode(hasRole(Role.Checkbox)).assertIsOff()
    }
}
