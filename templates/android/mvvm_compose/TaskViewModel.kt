package com.example.task.presentation

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.task.domain.Task
import com.example.task.domain.TaskRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

sealed interface TaskUiState {
    data object Loading : TaskUiState
    data object Empty : TaskUiState
    data class Success(val tasks: List<Task>) : TaskUiState
    data class Error(val message: String) : TaskUiState
}

@HiltViewModel
class TaskViewModel @Inject constructor(
    private val repository: TaskRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow<TaskUiState>(TaskUiState.Loading)
    val uiState: StateFlow<TaskUiState> = _uiState.asStateFlow()

    init {
        loadTasks()
    }

    fun loadTasks() {
        viewModelScope.launch {
            _uiState.value = TaskUiState.Loading
            repository.getTasks()
                .catch { e -> 
                    _uiState.value = TaskUiState.Error(e.localizedMessage ?: "Failed to load tasks") 
                }
                .collect { tasks -> 
                    _uiState.value = if (tasks.isEmpty()) {
                        TaskUiState.Empty
                    } else {
                        TaskUiState.Success(tasks)
                    }
                }
        }
    }

    fun toggleTask(id: String) {
        viewModelScope.launch {
            repository.toggleTaskCompletion(id)
        }
    }

    fun refresh() {
        loadTasks()
    }
}
