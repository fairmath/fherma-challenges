# Interview with Seunghu Kim and Eymen Ünay

As we continue series of conversations with FHERMA winners, today we talk with a team of Seunghu Kim (Chung-Ang Universitiy, Republic of Korea) and Eymen Ünay (University of Edinburgh), winners of Array Sorting challenge.

<table align="center" border="0" style="border-collapse: collapse; border: none;">
  <tr>
    <td align="center" style="border: none;">
      <img src="https://d2lkyury6zu01n.cloudfront.net/images/kim.png" width="200"/><br>
      <em>Seunghu Kim</em>
    </td>
    <td align="center" style="border: none;">
      <img src="https://d2lkyury6zu01n.cloudfront.net/images/unay.png" width="200"/><br>
      <em>Eymen Ünay</em>
    </td>
  </tr>
</table>

**Elvira:** *Thank you both for taking the time to speak with me today about your work on the *Fherma* platform. Before we discuss your solution, could you tell me what initially drew you to cryptography and fully homomorphic encryption (FHE)? Was there a particular moment, person, or course that inspired you to pursue this field?*

**Seunghu:** In my case, it was quite straightforward. As an undergraduate, I met a professor (Hyung Tae Lee, Chung-Ang University) who later became my advisor whose research focused on cryptography. I joined his lab as an intern, started exploring the field, and found it fascinating. That interest has stayed with me ever since.

**Eymen:** My path was slightly different. I come from a compiler research background and have always been interested in improving the performance of applications. FHE caught my attention precisely because it’s computationally intensive and it poses deep optimization challenges. I saw it as a domain where compiler research could make a tangible difference, which made it a compelling focus for my master’s work.

**Elvira:** *That’s a great combination of perspectives—one from cryptography, the other from systems and performance optimization. Could you each tell me a bit about your current research focus or academic work at the moment?*

**Seunghu:** Currently, I’m working on FHE, focusing on its applications and optimizations. My research interests also include developing its variants, such as threshold and multi-key schemes, as well as combining FHE with attribute-based encryption.

**Eymen:** My research now focuses on developing program representations and compilers that will optimize the speed and memory consumption of FHE programs. I am specifically interested in scaling FHE to larger programs with less resource consumption and increase its efficiency.

**Elvira:** *How long have you been working with FHE so far?*

**Seunghu:** About two years in total, though I started focusing specifically on FHE roughly a year ago.

**Eymen:** For me, it’s been around a year as well, but most of that time has been quite intensive because of the learning curve. The Fherma challenges actually became one of my main ways to apply what I was learning in real contexts.

**Elvira:** *How did you first discover the Fherma challenges platform? Were you actively looking for a competition, or did something in particular catch your eye?*

**Seunghu:** I had been using the OpenFHE library and following discussions on its community forum. That’s where I first saw an announcement about the Fherma challenges. I initially joined the matrix multiplication challenge, then later participated in the sorting challenge, which I found especially interesting.

**Eymen:** For me, it came through the OpenFHE paper itself. It mentioned Fherma and its challenges, and I realized it could be an excellent learning accelerator. I wasn’t specifically looking for a competition, but the structure, well-defined problems with measurable outcomes was ideal for applying theoretical knowledge to real implementations.

**Elvira:** *I understand you hadn’t met before joining the challenge but decided to collaborate during it. How did that come about?*

**Seunghu:** I was struggling with the implementation because my programming background isn’t very strong. Fortunately, the sorting challenge deadline was extended, and I saw Eymen’s message on Discord looking for a teammate. I reached out, and we started working together.

**Eymen:** Likewise, I had been facing challenges with FHE semantics and cryptographic details, since my expertise lies more in performance and application-level optimization. Collaborating with Seunghu provided exactly the balance I needed. His understanding of cryptography and my systems background complemented each other well, and that synergy became key to our final result.

**Elvira:** *That’s exactly the kind of collaboration we hoped to encourage through the platform -bringing together people with diverse expertise to solve complex problems. Could you walk us through your approach to the sorting problem in a way that would be understandable to technically minded readers who may not be specialists in FHE?*

**Eymen:** Certainly. Sorting an array whose elements are unknown to us is inherently challenging. A common strategy is to use hierarchical comparison structures (e.g., sorting networks), which can work but are prohibitively slow under FHE. We therefore redesigned the algorithm from first principles to minimize comparison depth, targeting a single-stage set of comparisons across all elements. In our final implementation, we effectively used one comparison primitive applied uniformly to the entire array, which substantially improved performance. We then used the resulting (still-encrypted) comparison outcomes to guide reordering: first constructing a permutation (equivalently, a rank array indicating each element’s target position) and then applying that permutation homomorphically to produce the sorted output.

**Seunghu:** Yes, as Eymen mentioned, we cannot observe individual comparison outcomes, so a data-oblivious sorting method is required. A standard option is a deterministic sorting network, but—as **Eymen** mentioned—it entails many sequential comparisons, which is impractical in the FHE setting. Our approach instead centers on the *rank* of each element (i.e., the number of smaller elements in the array). For ascending order, the rank directly corresponds to the element’s target index. Thus, we sort by computing ranks and then permuting accordingly, with our main optimization focused on accelerating the many pairwise comparisons needed to obtain those ranks.

**Elvira:** *What were the key difficulties or surprises you faced as you refined your rank-based FHE sorter?*

**Eymen:** Initially, our biggest challenge was just getting our solution to run on the platform. We discovered that execution times and memory limits behaved differently on our local machines than on the server, which took time to diagnose. Once we finally appeared on the leaderboard, though, it was highly motivating. Seeing the progress of other teams and the performance gap pushed us to refine our code and experiment with new optimizations. It also gave us a real sense of the competitive and collaborative spirit behind the platform.

**Seunghu:** I had a similar experience. I hadn’t realized how large the rotation keys in FHE could be, and I ran into several runtime errors. Seeing other participants’ performance, like hita’s, was motivating. We learned a lot from observing others’ optimizations and managed to achieve over a 15× improvement from our initial implementation.

**Elvira:** *That’s an impressive result. As you know, the platform publishes all challenge solutions as open source. What are your thoughts on sharing your work in that way? What role do you think open-source collaboration plays in advancing FHE research?*

**Eymen:** I think open-sourcing is absolutely essential, especially in FHE, where practical implementations are still limited. It helps researchers and developers see how theoretical constructs behave in practice. One thing I realized through this process is that performance can vary dramatically depending on factors like hardware, parameter selection, and even compiler settings. So while general-purpose APIs for FHE applications are valuable, they need to evolve alongside community contributions. The open model encourages precisely that kind of iterative improvement.

**Seunghu:** I agree completely. Open-sourcing our solution can benefit several applications, such as privacy-preserving auctions or k-nearest neighbor searches. Our method doesn’t require bootstrapping and performs well on smaller datasets (under about a thousand elements) so it could be directly useful for practical cases. Beyond that, sharing implementations makes the field more transparent and helps build a foundation for reproducible research in privacy-preserving computation.

**Elvira:** *Thank you again for sharing your time and your experience with the Fherma challenges. It’s been a pleasure hearing about your collaboration and your approach, and I look forward to seeing how your work develops in the future.*

**Eymen:** Thank you, it’s been a great experience.

**Seunghu:** Thank you very much.

---

Following our conversation, the team shared two pieces of good news: a paper derived from the challenge results is live on the ePrint Archive ([https://eprint.iacr.org/2025/1170](https://eprint.iacr.org/2025/1170)), and the sorting code behind it is now open-sourced ([https://github.com/oksuman/sorting-fhe](https://github.com/oksuman/sorting-fhe)). Yet another example of how FHERMA accelerates research.

If you're interested in FHE or privacy-preserving AI, you’re welcome to explore our current challenges at [[https://fherma.io/challenges](https://fherma.io/challenges)]. You can also revisit past challenges to experiment and try to develop improved solutions.

*Note: Past challenges are no longer eligible for prizes, but submitting improved solutions is encouraged as a way to sharpen your skills and help the community.*