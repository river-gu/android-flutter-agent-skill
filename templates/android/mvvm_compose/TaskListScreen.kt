package com.example.task.presentation

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.task.domain.Task

/**
 * 容器型 Composable：接入 ViewModel 与生命周期感知
 */
@Composable
fun TaskListScreen(
    viewModel: TaskViewModel,
    onNavigateToDetail: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    TaskListContent(
        uiState = uiState,
        onToggleTask = viewModel::toggleTask,
        onNavigateToDetail = onNavigateToDetail,
        onRetry = viewModel::refresh,
        modifier = modifier
    )
}

/**
 * 展示型 Composable：纯无状态函数，参数包含 modifier 首选参数与完整四态渲染
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TaskListContent(
    uiState: TaskUiState,
    onToggleTask: (String) -> Unit,
    onNavigateToDetail: (String) -> Unit,
    onRetry: () -> Unit,
    modifier: Modifier = Modifier
) {
    Scaffold(
        topBar = {
            TopAppBar(title = { Text(text = "Task Manager") })
        },
        modifier = modifier
    ) { padding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            when (val state = uiState) {
                is TaskUiState.Loading -> {
                    CircularProgressIndicator(modifier = Modifier.align(Alignment.Center))
                }
                is TaskUiState.Empty -> {
                    Column(
                        modifier = Modifier.align(Alignment.Center),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text(
                            text = "No tasks available. Tap to create one!",
                            style = MaterialTheme.typography.bodyLarge
                        )
                    }
                }
                is TaskUiState.Success -> {
                    LazyColumn(modifier = Modifier.fillMaxSize()) {
                        items(state.tasks, key = { it.id }) { task ->
                            ListItem(
                                headlineContent = { Text(task.title) },
                                supportingContent = { Text(task.description) },
                                leadingContent = {
                                    Checkbox(
                                        checked = task.isCompleted,
                                        onCheckedChange = { onToggleTask(task.id) }
                                    )
                                },
                                modifier = Modifier.clickable { onNavigateToDetail(task.id) }
                            )
                            HorizontalDivider()
                        }
                    }
                }
                is TaskUiState.Error -> {
                    Column(
                        modifier = Modifier.align(Alignment.Center),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text(text = state.message, color = MaterialTheme.colorScheme.error)
                        Spacer(modifier = Modifier.height(8.dp))
                        Button(onClick = onRetry) {
                            Text("Retry")
                        }
                    }
                }
            }
        }
    }
}
