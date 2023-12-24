use crate::err::ProcessingResult;
use crate::proc::MatchAction::*;
use crate::proc::MatchMode::*;
use crate::proc::Processor;
use crate::Cfg;
use aho_corasick::AhoCorasick;
use aho_corasick::AhoCorasickBuilder;
use css_minify::optimizations::Level;
use css_minify::optimizations::Minifier;
use lazy_static::lazy_static;
use std::str::from_utf8_unchecked;

lazy_static! {
  static ref STYLE_END: AhoCorasick = AhoCorasickBuilder::new()
    .ascii_case_insensitive(true)
    .build(["</style"]);
}

#[inline(always)]
pub fn process_style(proc: &mut Processor, cfg: &Cfg) -> ProcessingResult<()> {
  proc.require_not_at_end()?;
  let src = proc.m(WhileNotSeq(&STYLE_END), Discard);
  // `process_tag` will require closing tag.

  if cfg.minify_css {
    let result = Minifier::default()
      .minify(unsafe { from_utf8_unchecked(&proc[src]) }, Level::Three)
      .ok();
    // TODO Collect error as warning.
    if result.as_ref().filter(|r| r.len() < src.len()).is_some() {
      proc.write_slice(result.unwrap().as_bytes());
    } else {
      proc.write_range(src);
    };
  } else {
    proc.write_range(src);
  };

  Ok(())
}
