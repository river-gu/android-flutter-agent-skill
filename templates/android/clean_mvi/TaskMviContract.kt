package com.example.task.mvi

// Unidirectional Data Flow Contract
sealed interface TaskIntent {
    data object LoadTasks : TaskIntent
    data class ToggleTask(val id: String) : TaskIntent
    data class AddTask(val title: String) : TaskIntent
}

sealed interface TaskViewState {
    data object Idle : TaskViewState
    data object Loading : TaskViewState
    data class Success(val tasks: List<String>) : TaskViewState
    data class Error(val error: String) : TaskViewState
}

sealed interface TaskSingleEvent {
    data class ShowToast(val message: String) : TaskSingleEvent
    data class NavigateToDetail(val id: String) : TaskSingleEvent
}
