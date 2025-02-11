import ArgumentParser
import Foundation
import HomomorphicEncryption

struct FHEConfig: Codable {
    let scheme: String
    let indexesForRotationKey: [Int]
    let polyDegree: Int 
    let plaintextModulus: UInt64
    let coefficientModuli: [UInt64]
    
    enum CodingKeys: String, CodingKey {
        case scheme = "scheme"
        case indexesForRotationKey = "indexes_for_rotation_key"
        case polyDegree = "poly_degree"
        case plaintextModulus = "plaintext_modulus"
        case coefficientModuli = "coefficient_moduli"
    }
}

struct Tool: ParsableCommand {
    static let configuration = CommandConfiguration(
        abstract: "Solve challenge")

    @Option(name: [.customLong("config"), .customShort("c")],
            help: "Path to config file")
    var config: String

    @Option(name: [.customLong("key_eval"), .customShort("s")],
            help: "Path to secret key eval")
    var evalKey: String

    @Option(name: [.customLong("input1"), .customShort("h")],
            help: "Path to ciphertext")
    var ciphertext: String
    
   @Option(name: [.customLong("input2"), .customShort("h")],
            help: "Path to ciphertext2 - not used")
    var ciphertextnn: String

    @Option(name: [.customLong("output"), .customShort("r")],
            help: "Path to resulted json")
    var result: String

    mutating func run() {
        do {
            let cfg = try readCfg(cfg: config)

            let encryptParams = try EncryptionParameters<Bfv<UInt64>>(
                polyDegree: cfg.polyDegree,
                plaintextModulus: cfg.plaintextModulus,
                coefficientModuli: cfg.coefficientModuli.map { UInt64($0) },
                errorStdDev: .stdDev32,
                securityLevel: .quantum128
            )

            let context = try Context(encryptionParameters: encryptParams)

            var jsonData = try Data(contentsOf: URL(filePath: ciphertext ))
            let decodedJson = try JSONDecoder().decode(SerializedCiphertext<UInt64>.self, from: jsonData)
            let cipher: Bfv<UInt64>.CanonicalCiphertext = try Ciphertext(deserialize: decodedJson, context: context)
            let evalCiphertext = try cipher.convertToEvalFormat()

            // put your solution here
            
            let res = try evalCiphertext.convertToCanonicalFormat()

            jsonData = try JSONEncoder().encode(res.serialize())
            try jsonData.write(to: URL(fileURLWithPath: result))

            return

        } catch let error {
            print(error.localizedDescription)
        } 
    }

    private func readCfg(cfg: String) throws -> FHEConfig {
        let jsonData = try String(contentsOfFile: cfg, encoding: .utf8).data(using: .utf8)!
        let config = try JSONDecoder().decode(FHEConfig.self, from: jsonData)

        return config
    }
}

Tool.main()
