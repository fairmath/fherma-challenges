# Interview with Chi-Hieu Nguyen

As part of our ongoing interview series with FHERMA contributors, today we speak with Chi-Hieu Nguyen ([@hita](https://fherma.io/661f48decbb495aad204365c)), a Ph.D. researcher  at the University of Technology Sydney, who has already secured multiple wins on the platform. In this interview, we speak about his journey into the world of Fully Homomorphic Encryption (FHE), his hands-on experience with modern FHE libraries the Future of Privacy-Preserving Computation.
<p align="center">
  <img src="https://d2lkyury6zu01n.cloudfront.net/images/hieu.jpg" alt="photo" width="60%"/>
</p>

**Elvira (Fair Math):** Hi Hieu, thank you so much for joining us today. To start things off, could you share a bit about your background, how you got into the field of cryptography, and what initially led you to explore Fully Homomorphic Encryption (FHE)?

**Hieu:** Thank you for the invitation, Elvira. I'm glad to be here. For the question, I have been working on FHE since my first year of PhD. I remember it was about seven or eight months after I started. I was assigned to an ongoing paper by a former student. The project focused on integrating homomorphic encryption into a federated learning system to enhance system efficiency and performance.

It was a completely new topic to me at that time. It took me around six months to study the background on FHE schemes, understand the mathematical foundations, and gain hands-on experience with implementation. That was actually the hardest part, because there weren't many public libraries available.

I mainly use Python for my machine learning work, but I initially worked with Microsoft SEAL. In my opinion, it's a bit hard for beginners compared to the newer libraries like OpenFHE. At that time, OpenFHE didn't have a Python API, so it was a very hard experience debugging FHE programs. All the computation is done under encryption, so it's hard to trace where something goes wrong. But today we have several user-friendly libraries, with detailed documentation and better performance. We also have modern compilers that help users convert applications into FHE programs with minimal effort.

**Elvira:** It's impressive how much the tooling has evolved. And it sounds like those improvements are starting to pay off, we're seeing growing interest in privacy-preserving technologies. From your perspective, what are some of the most encouraging developments in this space, and how close do you think we are to broader adoption?

**Hieu:** I think FHE is getting more available for adoption. Tech companies like Apple have started using privacy-preserving computation in applications like private visual search and spam call detection. Companies like Microsoft, Google, and IBM are also exploring FHE integration, though some of it is still experimental. But I believe it's gaining more attention and will see more real-world adoption soon.

**Elvira:** Absolutely, that real-world traction is encouraging. Since you've had hands-on experience with different libraries, I'd love to dive into the developer side of things. Can you compare the FHE tools you've worked with? What makes a library more approachable or production-ready in your opinion?

**Hieu:** Yeah, so as I said, I started working with Microsoft SEAL. It was a bit hard to use. But now we have many open-source FHE libraries. Personally, I prefer OpenFHE. It comes with rich documentation, real hands-on examples, a well-structured code base, good performance with multi-threading, and an active community. So I think that's my most preferred library for now.

Another one I like is FHE Layers from IBM. It offers a very strong abstraction called tile tensor, which is efficient for many types of computation, especially linear transformations. I used it in some of my work in the Fherma Challenge, and it was quite successful.

**Elvira:** Great to hear some real-world perspective. On the topic of applied FHE: you've been very active in the Fherma Challenge, and your solutions are consistently top-performing. What draws you to these challenges, and is there one in particular that stands out?

**Hieu:** Each challenge is a unique and rewarding experience, but I would say I enjoyed the Invertible Matrix Challenge the most. Maybe because I was the only one who passed all the test cases, so I didn't have to worry too much about the performance afterwards. Just kidding.

I think it was interesting because it required a very different approach. Unlike other challenges where the idea is mostly about optimizing implementation, this one needed both a solid algorithmic strategy and an efficient implementation.

**Elvira:** Sounds like it really pushed both your algorithmic thinking and implementation skills — a rare combination. On the other hand, were there any challenges that you found particularly tough or frustrating to crack?

**Hieu:** Yes, the most difficult was probably the Array Sorting сhallenge. I remember in the first version, no one could solve it. We had to relax the constraints on time and accuracy to determine a winner.

The difficulty came from the very strict requirements, perhaps because the IBM team set a really high standard. So yes, that was the hardest one.

**Elvira:** Sometimes the toughest ones teach us the most! Outside of competitions, I know you're also doing academic research. What are you currently focusing on, and how are you thinking about the future of privacy-preserving machine learning?

**Hieu:** Right now, my research focuses on privacy-preserving machine learning. I'm applying FHE to a broad range of ML problems — supervised, unsupervised, reinforcement learning, and potentially generative AI in the future.

**Elvira:** That's exciting — especially the mention of generative AI, where trust and data confidentiality are becoming major concerns. Have you published any of your research, or is there somewhere fellow participants can explore your work? We'd love to include a link if there's anything available.

**Hieu:** You can explore my recent works through my [Google Scholar profile](https://scholar.google.com/citations?user=MqGsKf4AAAAJ). I also have some papers currently under review at Nature Machine Intelligence and IEEE Transactions. Please check back soon for updates on those works.

**Elvira:**  Thank you again for sharing your insights and experiences, Hieu. We're looking forward to seeing what you build next, both in research and in future challenges.

**Hieu:** Definitely. Thanks so much!

---

If you're interested in FHE or privacy-preserving AI, you're welcome to explore our [current challenges](https://fherma.io/challenges) and try solving them at your own pace. You can also revisit past challenges — and even take a shot at outperforming the all-time champion!

*Note: Past challenges are no longer eligible for prizes, but submitting improved solutions is still encouraged as a way to deepen your skills and support the community.*