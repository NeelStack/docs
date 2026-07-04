---
document_id: NES-400
title: React Native Standards
subtitle: Enterprise React Native, Mobile Architecture & Development Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Mobile Architecture Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-320 Frontend Reference Architecture
next_document: NES-401 Expo Architecture
---

# NES-400 — React Native Standards

> **"Single codebase, native speed, enterprise reliability. We write React Native code that behaves predictably across platforms."**

---

# Executive Summary

Mobile applications are a critical touchpoint for NeelStack customers.

To deliver high-performance, secure, and native-feeling experiences on both iOS and Android, we standardize on **React Native** as our primary mobile framework. 

This document defines the core architecture, coding practices, typescript rules, component lifecycle conventions, and platform-specific guidelines for building React Native applications at NeelStack.

Every mobile project must adhere to these standards to ensure long-term maintainability and high developer velocity.

---

# Purpose

This standard establishes:

- Core mobile technologies and packages
- TypeScript conventions for mobile
- Component structure and code organization
- Native vs. JS thread management principles
- iOS and Android platform consistency guidelines
- Code quality, formatting, and linting configurations

---

# Core Principles

Every React Native application must be:

✓ **Native-Feeling**: Follow platform design behaviors (e.g., keyboard handling, gesture responses).

✓ **Type Safe**: End-to-end typing from API requests to component props.

✓ **Performant**: Keep the JavaScript thread clear of heavy processing to avoid frame drops.

✓ **Observable**: Capture crashes, telemetry, and analytical events reliably.

✓ **Maintainable**: Keep styles, state, and UI logic modular and isolated.

---

# Tech Stack & Package Standards

We lock specific library versions to prevent fragmentation across mobile products:

| Area | Approved Library | Rationale |
|---|---|---|
| Core Framework | React Native (latest stable) | Cross-platform UI rendering |
| App Runtime | Expo (Managed Workflow) | Accelerates DX and simplifies builds |
| Styling | StyleSheet / NativeWind | Tailwind CSS utility styling |
| State | Zustand + TanStack Query | Client & server state isolation |
| Navigation | Expo Router | Native file-based navigation |
| Safe Area | react-native-safe-area-context | Correct screen padding across device notches |

---

# Coding Standards & Guidelines

## TypeScript Configuration

All code must be written in TypeScript with strict null checks enabled.

- Avoid the `any` type at all costs. Use `unknown` with type guards if the type is dynamic.
- Declare prop interfaces explicitly for every component.

```typescript
interface ButtonProps {
  label: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  label,
  onPress,
  variant = 'primary',
  disabled = false,
}) => {
  return (
    <TouchableOpacity onPress={onPress} disabled={disabled}>
      <Text>{label}</Text>
    </TouchableOpacity>
  );
};
```

---

# Component Best Practices

1. **Use Functional Components**: Class components are legacy and prohibited.
2. **Minimize Inline Functions**: Avoid defining functions directly in JSX props to prevent unnecessary re-renders. Use `useCallback` for event handlers passed to complex children.
3. **Use Primitive Components**: Standardize on `View`, `Text`, `Image`, `Pressable`, and `TextInput`. 
4. **Prefer Pressable**: Avoid `TouchableOpacity` for new components; `Pressable` provides a more customizable API for tap states and interactions.

---

# Platform-Specific Code Handling

To write cross-platform code while respecting platform design patterns:

- **Extension Files**: Use `.ios.tsx` and `.android.tsx` extension files for large platform differences.
- **Platform Module**: Use `Platform.OS` or `Platform.select` for inline styling or simple logical branching.

```typescript
import { Platform, StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  container: {
    paddingTop: Platform.select({
      ios: 20,
      android: 0,
    }),
  },
});
```

---

# Thread Management & Performance

React Native operates on two primary threads: the **JavaScript Thread** and the **Native/UI Thread**.

- **JS Thread**: Where your React code, API calls, and logic execute.
- **UI Thread**: Where native view rendering, UI rendering, layout computation, and native animations run.

### Standard rules:
- **Never block the JS thread**: Keep computational tasks, large object mapping, or complex calculations off the JS thread during layout transitions.
- **Use Native Animations**: Set `useNativeDriver: true` for all Animated API transitions to offload them to the UI thread.
- **Debound Input Handlers**: Debounce search fields or fast text changes to avoid thrashing the JS thread.

---

# Anti-Patterns

❌ **Hardcoded UI Sizes**: Do not use absolute pixel values that break on smaller devices. Use responsive percentages, flex layouts, or the design system spacing tokens.

❌ **Ignoring Safe Areas**: Writing layouts that render underneath the camera notch or system home indicator.

❌ **Using ScrollView for Long Lists**: Using `ScrollView` instead of `FlatList` or `FlashList` for large arrays of data, which causes high memory usage and app crashes.

❌ **Overusing Native Libraries**: Installing native-linked packages for features that can be implemented cleanly in JavaScript, which complicates the native build.

---

# Production Checklist

- [ ] All code conforms to strict TypeScript compiler options.
- [ ] Platform checks are verified on both an iOS simulator and an Android emulator.
- [ ] Safe Area views wrap all top-level layouts.
- [ ] KeyboardAvoidingView is configured correctly for form pages.
- [ ] All animations use native drivers.
- [ ] ESLint and Prettier check runs pass.

---

# Success Criteria

The React Native setup is successful when:
- Mobile apps build cleanly for both iOS and Android with a shared codebase exceeding 90% code reuse.
- Frame rates remain stable at 60 FPS (or 120 FPS on high-refresh screens) on mid-tier test devices.
- Developers can configure and spin up a new local emulator within 15 minutes of onboarding.
- Standard coding conventions are enforced automatically via CI linting gates.

---

# Future Evolution

Version 2.0 will include:
- Native modules creation guide using Expo Autolinking
- Fabric Architecture and TurboModules transition plan
- React Server Components (RSC) on mobile integration blueprint
- Architecture fitness tests for component sizes and render limits
- Unified web and mobile styling sharing configurations

---

# Mobile Standards Checklist

- [x] Tech Stack & Package Standards Defined
- [x] TypeScript Standards Configured
- [x] Component Best Practices Detailed
- [x] Platform-Specific Code Conventions Set
- [x] Native/JS Thread Guidelines Documented
- [x] Anti-patterns & Production Checklist Completed
- [x] Success Criteria Defined

---

# Document Status

**Document:** NES-400 — React Native Standards
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-401 — Expo Architecture**
