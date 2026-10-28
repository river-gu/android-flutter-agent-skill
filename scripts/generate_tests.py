#!/usr/bin/env python3
"""
Automated Test Generator for Android and Flutter
Generates unit tests, Compose/Widget UI tests, and Maestro E2E test scripts.
"""

import sys
import argparse
import re
from pathlib import Path


ANDROID_VM_TEST_TEMPLATE = """package {package_name}.presentation

import app.cash.turbine.test
import io.mockk.coEvery
import io.mockk.mockk
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.*
import org.junit.After
import org.junit.Assert.assertEquals
import org.junit.Before
import org.junit.Test

@OptIn(ExperimentalCoroutinesApi::class)
class {feature_name}ViewModelTest {{

    private val testDispatcher = StandardTestDispatcher()
    private lateinit var viewModel: {feature_name}ViewModel

    @Before
    fun setUp() {{
        Dispatchers.setMain(testDispatcher)
        viewModel = {feature_name}ViewModel()
    }}

    @After
    fun tearDown() {{
        Dispatchers.resetMain()
    }}

    @Test
    fun `loadInitialData emits Loading then Success state`() = runTest(testDispatcher) {{
        viewModel.uiState.test {{
            assertEquals({feature_name}UiState.Loading, awaitItem())

            testScheduler.advanceUntilIdle()

            val success = awaitItem() as {feature_name}UiState.Success
            assertEquals("Hello from {feature_name}", success.data)

            cancelAndIgnoreRemainingEvents()
        }}
    }}
}}
"""

ANDROID_UI_TEST_TEMPLATE = """package {package_name}.presentation

import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createComposeRule
import io.mockk.every
import io.mockk.mockk
import kotlinx.coroutines.flow.MutableStateFlow
import org.junit.Rule
import org.junit.Test

class {feature_name}ScreenTest {{

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun screen_displaysTitleAndContent_whenStateIsSuccess() {{
        val fakeFlow = MutableStateFlow({feature_name}UiState.Success("Mock Data"))
        val mockViewModel = mockk<{feature_name}ViewModel>(relaxed = true) {{
            every {{ uiState }} returns fakeFlow
        }}

        composeTestRule.setContent {{
            {feature_name}Screen(viewModel = mockViewModel)
        }}

        composeTestRule.onNodeWithText("{feature_name}").assertIsDisplayed()
        composeTestRule.onNodeWithText("Content Loaded: Mock Data").assertIsDisplayed()
    }}

    @Test
    fun screen_displaysLoadingIndicator_whenStateIsLoading() {{
        val fakeFlow = MutableStateFlow({feature_name}UiState.Loading)
        val mockViewModel = mockk<{feature_name}ViewModel>(relaxed = true) {{
            every {{ uiState }} returns fakeFlow
        }}

        composeTestRule.setContent {{
            {feature_name}Screen(viewModel = mockViewModel)
        }}

        composeTestRule.onNode(hasProgressBarRangeInfo(ProgressBarRangeInfo.Indeterminate))
            .assertIsDisplayed()
    }}
}}
"""

FLUTTER_BLOC_TEST_TEMPLATE = """import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import '{feature_snake}_bloc.dart';

void main() {{
  group('{feature_name}Bloc Unit Tests', () {{
    late {feature_name}Bloc bloc;

    setUp(() {{
      bloc = {feature_name}Bloc();
    }});

    tearDown(() {{
      bloc.close();
    }});

    test('initial state is {feature_name}Initial', () {{
      expect(bloc.state, isA<{feature_name}Initial>());
    }});

    blocTest<{feature_name}Bloc, {feature_name}State>(
      'emits [{feature_name}Loading, {feature_name}Success] on {feature_name}Started',
      build: () => bloc,
      act: (b) => b.add({feature_name}Started()),
      expect: () => [
        isA<{feature_name}Loading>(),
        isA<{feature_name}Success>().having((s) => s.data, 'data', 'Loaded {feature_name} Data'),
      ],
    );
  }});
}}
"""

FLUTTER_WIDGET_TEST_TEMPLATE = """import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import '{feature_snake}_page.dart';

void main() {{
  group('{feature_name}Page Widget UI Tests', () {{
    testWidgets('renders title and loading state initially', (tester) async {{
      await tester.pumpWidget(
        const MaterialApp(home: {feature_name}Page()),
      );

      expect(find.text('{feature_name}'), findsOneWidget);
      expect(find.byType(CircularProgressIndicator), findsOneWidget);

      await tester.pumpAndSettle();
      expect(find.text('Loaded {feature_name} Data'), findsOneWidget);
    }});
  }});
}}
"""

MAESTRO_E2E_TEMPLATE = """appId: {package_name}
---
- launchApp
- assertVisible: "{feature_name}"
- takeScreenshot: {feature_snake}_screen_loaded
"""


def to_snake_case(name: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


def generate_android_tests(out_dir: Path, name: str, pkg: str, test_type: str):
    out_dir.mkdir(parents=True, exist_ok=True)
    snake = to_snake_case(name)

    if test_type in ["unit", "all"]:
        vm_test = out_dir / f"{name}ViewModelTest.kt"
        vm_test.write_text(ANDROID_VM_TEST_TEMPLATE.format(feature_name=name, package_name=pkg))
        print(f"✅ Generated Android ViewModel Unit Test: {vm_test}")

    if test_type in ["ui", "all"]:
        ui_test = out_dir / f"{name}ScreenTest.kt"
        ui_test.write_text(ANDROID_UI_TEST_TEMPLATE.format(feature_name=name, package_name=pkg))
        print(f"✅ Generated Android Compose UI Test: {ui_test}")

    if test_type in ["e2e", "all"]:
        e2e_test = out_dir / f"{snake}_e2e.yaml"
        e2e_test.write_text(MAESTRO_E2E_TEMPLATE.format(feature_name=name, feature_snake=snake, package_name=pkg))
        print(f"✅ Generated Maestro E2E Test: {e2e_test}")


def generate_flutter_tests(out_dir: Path, name: str, test_type: str):
    out_dir.mkdir(parents=True, exist_ok=True)
    snake = to_snake_case(name)

    if test_type in ["unit", "all"]:
        unit_test = out_dir / f"{snake}_bloc_test.dart"
        unit_test.write_text(FLUTTER_BLOC_TEST_TEMPLATE.format(feature_name=name, feature_snake=snake))
        print(f"✅ Generated Flutter BLoC Unit Test: {unit_test}")

    if test_type in ["ui", "all"]:
        widget_test = out_dir / f"{snake}_page_test.dart"
        widget_test.write_text(FLUTTER_WIDGET_TEST_TEMPLATE.format(feature_name=name, feature_snake=snake))
        print(f"✅ Generated Flutter Widget UI Test: {widget_test}")

    if test_type in ["e2e", "all"]:
        e2e_test = out_dir / f"{snake}_e2e.yaml"
        e2e_test.write_text(MAESTRO_E2E_TEMPLATE.format(feature_name=name, feature_snake=snake, package_name="com.example.app"))
        print(f"✅ Generated Maestro E2E Test: {e2e_test}")


def main():
    parser = argparse.ArgumentParser(description="Automated Test Generator for Android & Flutter")
    parser.add_argument("--platform", choices=["android", "flutter"], required=True)
    parser.add_argument("--name", required=True, help="Feature name (e.g. TaskList)")
    parser.add_argument("--type", choices=["unit", "ui", "e2e", "all"], default="all", help="Test type")
    parser.add_argument("--output", default=".", help="Output directory")
    parser.add_argument("--package", default="com.example.app", help="Android package name")

    args = parser.parse_args()
    out_dir = Path(args.output)

    if args.platform == "android":
        generate_android_tests(out_dir, args.name, args.package, args.type)
    else:
        generate_flutter_tests(out_dir, args.name, args.type)


if __name__ == "__main__":
    main()
