# Adaptive & Responsive Layouts Guide (折叠屏、平板与响应式多端适配)

随着折叠屏手机（Foldables）、横屏设备与平板电脑的普及，移动端应用必须避免只按“竖屏窄屏手机”硬编码设计。

---

## 一、断点标准与视口级别 (Breakpoints)

业界统一采纳 Material Design 3 的窗口尺寸类（Window Size Classes）标准：

| 视口尺寸类 | 宽度范围 (dp) | 典型设备场景 | 推荐布局模式 |
|---|---|---|---|
| **Compact** | `< 600dp` | 普通单手手机竖屏 | 单一纵向堆叠流，单列列表，底部导航 (NavigationBar) |
| **Medium** | `600dp ~ 839dp` | 折叠屏展开态、小型平板、小尺寸手机横屏 | 列表/详情联动，侧边导航栏 (NavigationRail)，网格并列 |
| **Expanded** | `>= 840dp` | 大型平板、折叠屏横屏、桌面端 (Desktop) | 永久侧边导航抽屉 (PermanentDrawer)，主次双栏/三栏多窗格 |

---

## 二、Android Jetpack Compose 响应式规范

### 1. 视口状态注入
* 引入依赖：`androidx.compose.material3:material3-window-size-class`
* 在 Activity 顶层计算 `calculateWindowSizeClass(this)` 并通过 `CompositionLocal` 或参数逐层下发。

### 2. 避免的坏味道与反模式
* ❌ 严禁死写固定宽度（如 `Modifier.width(360.dp)`），在折叠屏展开时会导致大面积白边。
* ❌ 严禁在所有设备上一律使用全屏 Modal/Dialog，在平板上应采用有最大宽度约束的中置卡片。
* ✅ 推荐使用官方 **List-Detail Pane** 布局模式：
  - 在 `Compact` 屏幕上，点击列表项跳转至全屏详情页。
  - 在 `Medium` 或 `Expanded` 屏幕上，左侧展示列表，右侧固定展示详情面板。

见模版：[AdaptiveListDetailScreen.kt](../templates/android/adaptive/AdaptiveListDetailScreen.kt)

---

## 三、Flutter 响应式规范

### 1. 禁用硬编码与滥用 MediaQuery
* ❌ **反模式**：`double screenWidth = MediaQuery.of(context).size.width * 0.8;`
  * 缺陷：当用户分屏或平板旋转时，`MediaQuery` 会触发整个顶层页面全量重组。
* ✅ **推荐规范**：使用 `LayoutBuilder` 局部感知父容器的 `constraints`：
```dart
Widget build(BuildContext context) {
  return LayoutBuilder(
    builder: (context, constraints) {
      if (constraints.maxWidth >= 840) {
        return const ExpandedDashboardView();
      } else if (constraints.maxWidth >= 600) {
        return const MediumSplitView();
      } else {
        return const CompactSingleColumnView();
      }
    },
  );
}
```
