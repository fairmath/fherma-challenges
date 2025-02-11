// swift-tools-version: 6.0
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "app",
    products: [
        .executable(name: "app", targets: ["app"]),
    ],
    dependencies: [
        .package(url: "https://github.com/apple/swift-homomorphic-encryption.git", from: "1.0.2"),
        .package(url: "https://github.com/apple/swift-argument-parser.git", from: "1.5.0")
    ],
    targets: [
        .executableTarget(
            name: "app",
            dependencies: [
                .product(name: "HomomorphicEncryption", package: "swift-homomorphic-encryption"),
                .product(name: "ArgumentParser", package: "swift-argument-parser")
            ],
            swiftSettings: [.unsafeFlags(["-cross-module-optimization"],
                .when(configuration: .release))]
        ),
    ]
)