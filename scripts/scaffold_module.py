#!/usr/bin/env python3
"""
Scaffold Feature Module for Android or Flutter
Quickly generates clean architecture boilerplate files.
"""

import sys
import argparse
from pathlib import Path


ANDROID_COMPOSE_TEMPLATE = """package {package_name}.presentation

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle

@Composable
fun {feature_name}Screen(
    viewModel: {feature_name}ViewModel,
    modifier: Modifier = Modifier
) {{
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    Scaffold(
        topBar = {{
            TopAppBar(title = {{ Text("{feature_name}") }})
        }}
    ) {{ innerPadding ->
        Box(
            modifier = modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(16.dp)
        ) {{
            when (val state = uiState) {{
                is {feature_name}UiState.Loading -> CircularProgressIndicator()
                is {feature_name}UiState.Success -> Text("Content Loaded: ${{state.data}}")
                is {feature_name}UiState.Error -> Text("Error: ${{state.message}}", color = MaterialTheme.colorScheme.error)
            }}
        }}
    }}
}}
"""

ANDROID_VIEWMODEL_TEMPLATE = """package {package_name}.presentation

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

sealed interface {feature_name}UiState {{
    data object Loading : {feature_name}UiState
    data class Success(val data: String) : {feature_name}UiState
    data class Error(val message: String) : {feature_name}UiState
}}

@HiltViewModel
class {feature_name}ViewModel @Inject constructor() : ViewModel() {{
    private val _uiState = MutableStateFlow<{feature_name}UiState>({feature_name}UiState.Loading)
    val uiState: StateFlow<{feature_name}UiState> = _uiState.asStateFlow()

    init {{
        loadInitialData()
    }}

    fun loadInitialData() {{
        viewModelScope.launch {{
            _uiState.value = {feature_name}UiState.Loading
            try {{
                // Simulating repository query
                _uiState.value = {feature_name}UiState.Success("Hello from {feature_name}")
            }} catch (e: Exception) {{
                _uiState.value = {feature_name}UiState.Error(e.localizedMessage ?: "Unknown error")
            }}
        }}
    }}
}}
"""

FLUTTER_BLOC_TEMPLATE = """import 'package:flutter_bloc/flutter_bloc.dart';

// Events
sealed class {feature_name}Event {{}}
final class {feature_name}Started extends {feature_name}Event {{}}

// States
sealed class {feature_name}State {{}}
final class {feature_name}Initial extends {feature_name}State {{}}
final class {feature_name}Loading extends {feature_name}State {{}}
final class {feature_name}Success extends {feature_name}State {{
  final String data;
  {feature_name}Success(this.data);
}}
final class {feature_name}Failure extends {feature_name}State {{
  final String message;
  {feature_name}Failure(this.message);
}}

// Bloc
class {feature_name}Bloc extends Bloc<{feature_name}Event, {feature_name}State> {{
  {feature_name}Bloc() : super({feature_name}Initial()) {{
    on<{feature_name}Started>((event, emit) async {{
      emit({feature_name}Loading());
      try {{
        await Future.delayed(const Duration(milliseconds: 300));
        emit({feature_name}Success('Loaded {feature_name} Data'));
      }} catch (e) {{
        emit({feature_name}Failure(e.toString()));
      }}
    }});
  }}
}}
"""

FLUTTER_PAGE_TEMPLATE = """import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '{feature_snake}_bloc.dart';

class {feature_name}Page extends StatelessWidget {{
  const {feature_name}Page({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return BlocProvider(
      create: (context) => {feature_name}Bloc()..add({feature_name}Started()),
      child: Scaffold(
        appBar: AppBar(title: const Text('{feature_name}')),
        body: BlocBuilder<{feature_name}Bloc, {feature_name}State>(
          builder: (context, state) {{
            return switch (state) {{
              {feature_name}Initial() || {feature_name}Loading() =>
                const Center(child: CircularProgressIndicator()),
              {feature_name}Success(:final data) =>
                Center(child: Text(data)),
              {feature_name}Failure(:final message) =>
                Center(child: Text('Error: $message', style: const TextStyle(color: Colors.red))),
            }};
          }},
        ),
      ),
    );
  }}
}}
"""


def to_snake_case(name: str) -> str:
    import re
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


def scaffold_android(out_dir: Path, name: str, pkg: str):
    feat_dir = out_dir / to_snake_case(name)
    pres_dir = feat_dir / "presentation"
    pres_dir.mkdir(parents=True, exist_ok=True)

    screen_file = pres_dir / f"{name}Screen.kt"
    vm_file = pres_dir / f"{name}ViewModel.kt"

    screen_file.write_text(ANDROID_COMPOSE_TEMPLATE.format(feature_name=name, package_name=pkg))
    vm_file.write_text(ANDROID_VIEWMODEL_TEMPLATE.format(feature_name=name, package_name=pkg))

    print(f"✅ Generated Android Compose feature '{name}' at {feat_dir}")


def scaffold_flutter(out_dir: Path, name: str):
    snake = to_snake_case(name)
    feat_dir = out_dir / snake
    feat_dir.mkdir(parents=True, exist_ok=True)

    bloc_file = feat_dir / f"{snake}_bloc.dart"
    page_file = feat_dir / f"{snake}_page.dart"

    bloc_file.write_text(FLUTTER_BLOC_TEMPLATE.format(feature_name=name))
    page_file.write_text(FLUTTER_PAGE_TEMPLATE.format(feature_name=name, feature_snake=snake))

    print(f"✅ Generated Flutter BLoC feature '{name}' at {feat_dir}")


def main():
    parser = argparse.ArgumentParser(description="Scaffold Android / Flutter Feature Module")
    parser.add_argument("--platform", choices=["android", "flutter"], required=True)
    parser.add_argument("--name", required=True, help="Feature name in PascalCase (e.g. TaskList)")
    parser.add_argument("--output", default=".", help="Output directory")
    parser.add_argument("--package", default="com.example.app", help="Android package name")

    args = parser.parse_args()
    out_dir = Path(args.output)

    if args.platform == "android":
        scaffold_android(out_dir, args.name, args.package)
    else:
        scaffold_flutter(out_dir, args.name)


if __name__ == "__main__":
    main()
