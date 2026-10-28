package com.example.core.adaptive

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.material3.windowsizeclass.WindowWidthSizeClass
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

data class ItemData(val id: String, val title: String, val detail: String)

/**
 * 响应式双窗格（List-Detail）组件：
 * - Compact (普通手机): 单栏列表，点击回调触发导航
 * - Medium / Expanded (折叠屏/平板): 左右分屏联动
 */
@Composable
fun AdaptiveListDetailScreen(
    windowWidthSizeClass: WindowWidthSizeClass,
    items: List<ItemData>,
    onNavigateToDetail: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    val isExpanded = windowWidthSizeClass != WindowWidthSizeClass.Compact
    var selectedItemId by remember { mutableStateOf(items.firstOrNull()?.id) }

    if (isExpanded) {
        // 双窗格左右分屏 (平板 / 折叠屏展开)
        Row(modifier = modifier.fillMaxSize()) {
            Box(modifier = Modifier.weight(0.4f).fillMaxHeight()) {
                LazyColumn(modifier = Modifier.fillMaxSize()) {
                    items(items, key = { it.id }) { item ->
                        ListItem(
                            headlineContent = { Text(item.title) },
                            modifier = Modifier.clickable { selectedItemId = item.id },
                            colors = ListItemDefaults.colors(
                                containerColor = if (item.id == selectedItemId) {
                                    MaterialTheme.colorScheme.primaryContainer
                                } else {
                                    MaterialTheme.colorScheme.surface
                                }
                            )
                        )
                        HorizontalDivider()
                    }
                }
            }

            VerticalDivider(modifier = Modifier.fillMaxHeight().width(1.dp))

            Box(
                modifier = Modifier
                    .weight(0.6f)
                    .fillMaxHeight()
                    .padding(24.dp),
                contentAlignment = Alignment.TopStart
            ) {
                val currentItem = items.find { it.id == selectedItemId }
                if (currentItem != null) {
                    Column {
                        Text(text = currentItem.title, style = MaterialTheme.typography.headlineMedium)
                        Spacer(modifier = Modifier.height(16.dp))
                        Text(text = currentItem.detail, style = MaterialTheme.typography.bodyLarge)
                    }
                } else {
                    Text(text = "Select an item to view details")
                }
            }
        }
    } else {
        // 单窗格纵向流 (普通手机)
        LazyColumn(modifier = modifier.fillMaxSize()) {
            items(items, key = { it.id }) { item ->
                ListItem(
                    headlineContent = { Text(item.title) },
                    modifier = Modifier.clickable { onNavigateToDetail(item.id) }
                )
                HorizontalDivider()
            }
        }
    }
}
